import argparse
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

import openai
import requests
from openai import OpenAI
from tavily import TavilyClient

AGENT_SYSTEM_PROMPT = """
You are an intelligent travel assistant. Your task is to analyze user requests and use available tools to solve problems step by step.

# Available Tools:
- `get_weather(city: str)`: Query real-time weather for a specified city.
- `get_attraction(city: str, weather: str, preference: str = "", budget: str = "")`: Search for recommended tourist attractions based on city, weather, preference, and budget.
- `check_ticket_availability(attraction: str)`: Check whether tickets for the recommended attraction are available.
- `save_preference(preference: str, budget: str = "")`: Save user preference and budget into memory.
- `adjust_strategy(reason: str)`: Adjust recommendation strategy after repeated rejection.

# Output Format Requirements:
Each response must strictly follow this format, containing one Thought-Action pair:

Thought: [Your thinking process and next step plan]
Action: [The specific action you want to execute]

Action format must be one of the following:
1. Call a tool: function_name(arg_name="arg_value")
2. Finish task: Finish[final answer]

# Important Notes:
- Output only one Thought-Action pair each time
- Action must be on the same line, do not break lines
- When you have collected enough information to answer the user's question, you must use Action: Finish[final answer] format to end
""".strip()


@dataclass
class Memory:
    preferences: list[str] = field(default_factory=list)
    budget: str = ""
    rejected_recommendations: list[str] = field(default_factory=list)
    strategy_note: str = ""

    def summary(self) -> str:
        parts: list[str] = []
        if self.preferences:
            parts.append(f"Preferences: {', '.join(self.preferences)}")
        if self.budget:
            parts.append(f"Budget: {self.budget}")
        if self.rejected_recommendations:
            parts.append(
                "Rejected recommendations: " + ", ".join(self.rejected_recommendations)
            )
        if self.strategy_note:
            parts.append(f"Strategy note: {self.strategy_note}")
        return " | ".join(parts) if parts else "No saved memory."


class OpenAICompatibleClient:
    def __init__(self, model: str, api_key: str, base_url: str):
        self.model = model
        self.api_key = api_key
        self.base_url = normalize_openai_base_url(base_url)
        self.client = OpenAI(api_key=api_key, base_url=self.base_url)

    def generate(self, prompt: str, system_prompt: str) -> str:
        print("Calling large language model...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                stream=False,
            )
        except openai.AuthenticationError as exc:
            raise SystemExit(
                "OpenAI authentication failed. Please verify OPENAI_API_KEY is valid for the configured endpoint. "
                f"Details: {exc}"
            ) from exc
        except openai.PermissionDeniedError as exc:
            raise SystemExit(
                "OpenAI request was blocked by the service provider. Please check account permissions, IP restrictions, "
                "or security policies on OPENAI_BASE_URL; and confirm OPENAI_MODEL is available for your key. "
                f"Details: {exc}"
            ) from exc
        except openai.NotFoundError as exc:
            raise SystemExit(
                "Model or endpoint not found. Please verify OPENAI_BASE_URL and OPENAI_MODEL. "
                f"Details: {exc}"
            ) from exc
        except openai.RateLimitError as exc:
            raise SystemExit(
                "Rate limit exceeded. Please retry later or reduce request frequency. "
                f"Details: {exc}"
            ) from exc
        except openai.BadRequestError as exc:
            raise SystemExit(
                "Request rejected as invalid by provider. Please check prompt/content policy and model compatibility. "
                f"Details: {exc}"
            ) from exc
        except openai.APIConnectionError as exc:
            raise SystemExit(
                "Failed to connect to OpenAI-compatible endpoint. Please verify OPENAI_BASE_URL and network connectivity. "
                f"Details: {exc}"
            ) from exc
        answer = response.choices[0].message.content or ""
        print("Large language model responded successfully.")
        return answer


class TravelAssistantAgent:
    def __init__(self, llm: OpenAICompatibleClient):
        self.llm = llm
        self.memory = Memory()
        self.rejection_count = 0
        self.available_tools = {
            "get_weather": self.get_weather,
            "get_attraction": self.get_attraction,
            "check_ticket_availability": self.check_ticket_availability,
            "save_preference": self.save_preference,
            "adjust_strategy": self.adjust_strategy,
        }

    def get_weather(self, city: str) -> str:
        url = f"https://wttr.in/{city}?format=j1"
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            current_condition = data["current_condition"][0]
            weather_desc = current_condition["weatherDesc"][0]["value"]
            temp_c = current_condition["temp_C"]
            return f"{city} current weather: {weather_desc}, temperature {temp_c} degrees Celsius"
        except requests.exceptions.RequestException as exc:
            return f"Error: Network problem encountered when querying weather - {exc}"
        except (KeyError, IndexError, ValueError) as exc:
            return f"Error: Failed to parse weather data, city name may be invalid - {exc}"

    def get_attraction(
        self,
        city: str,
        weather: str,
        preference: str = "",
        budget: str = "",
    ) -> str:
        api_key = os.environ.get("TAVILY_API_KEY")
        if not api_key:
            return "Error: TAVILY_API_KEY environment variable not configured."

        tavily = TavilyClient(api_key=api_key)
        memory_preference = preference or ", ".join(self.memory.preferences)
        memory_budget = budget or self.memory.budget
        query_parts = [
            f"best tourist attractions in {city}",
            f"suitable for {weather} weather",
        ]
        if memory_preference:
            query_parts.append(f"matching preference: {memory_preference}")
        if memory_budget:
            query_parts.append(f"budget: {memory_budget}")
        if self.memory.strategy_note:
            query_parts.append(self.memory.strategy_note)
        query = ", ".join(query_parts)

        try:
            response = tavily.search(query=query, search_depth="basic", include_answer=True)
            if response.get("answer"):
                return response["answer"]

            formatted_results = []
            for result in response.get("results", []):
                formatted_results.append(f"- {result['title']}: {result['content']}")
            if not formatted_results:
                return "Sorry, no relevant tourist attraction recommendations found."
            return "Based on search, found the following information for you:\n" + "\n".join(
                formatted_results
            )
        except Exception as exc:
            return f"Error: Problem occurred when executing Tavily search - {exc}"

    def check_ticket_availability(self, attraction: str) -> str:
        sold_out_keywords = ("forbidden city", "popular museum")
        if attraction.lower() in sold_out_keywords:
            return f"Tickets for {attraction} are sold out. Please recommend an alternative."
        return f"Tickets for {attraction} are currently available."

    def save_preference(self, preference: str, budget: str = "") -> str:
        if preference and preference not in self.memory.preferences:
            self.memory.preferences.append(preference)
        if budget:
            self.memory.budget = budget
        return f"Saved preference: {preference or 'N/A'}, budget: {budget or 'N/A'}"

    def adjust_strategy(self, reason: str) -> str:
        self.memory.strategy_note = (
            f"Adjust recommendation strategy because {reason}. Prefer alternatives that differ in style, budget, or indoor/outdoor profile."
        )
        return self.memory.strategy_note

    def reject_recommendation(self, attraction: str) -> None:
        self.rejection_count += 1
        self.memory.rejected_recommendations.append(attraction)
        if self.rejection_count >= 3:
            self.adjust_strategy("the user rejected three consecutive recommendations")

    def run(self, user_prompt: str, max_loops: int = 5) -> str:
        prompt_history = [f"User request: {user_prompt}", f"Memory: {self.memory.summary()}"]
        print(f"User input: {user_prompt}\n{'=' * 40}")

        for i in range(max_loops):
            print(f"--- Loop {i + 1} ---\n")
            full_prompt = "\n".join(prompt_history)
            llm_output = self.llm.generate(full_prompt, system_prompt=AGENT_SYSTEM_PROMPT)
            match = re.search(
                r"(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)",
                llm_output,
                re.DOTALL,
            )
            if match:
                llm_output = match.group(1).strip()
            print(f"Model output:\n{llm_output}\n")
            prompt_history.append(llm_output)

            action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
            if not action_match:
                observation_str = "Observation: Error: No action found."
                print(f"{observation_str}\n{'=' * 40}")
                prompt_history.append(observation_str)
                continue

            action_str = action_match.group(1).strip()
            if action_str.startswith("Finish"):
                final_answer_match = re.match(r"Finish\[(.*)\]", action_str, re.DOTALL)
                final_answer = final_answer_match.group(1) if final_answer_match else action_str
                print(f"Task completed, final answer: {final_answer}")
                return final_answer

            tool_name_match = re.search(r"(\w+)\(", action_str)
            args_match = re.search(r"\((.*)\)", action_str)
            if not tool_name_match or not args_match:
                observation = "Error: Invalid action format."
            else:
                tool_name = tool_name_match.group(1)
                kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_match.group(1)))
                tool = self.available_tools.get(tool_name)
                observation = tool(**kwargs) if tool else f"Error: Undefined tool '{tool_name}'"

            observation_str = f"Observation: {observation}"
            print(f"{observation_str}\n{'=' * 40}")
            prompt_history.append(observation_str)

        return "Reached the maximum number of loops without finishing the task."


def normalize_openai_base_url(base_url: str) -> str:
    normalized = base_url.rstrip("/")
    for suffix in ("/chat/completions", "/responses", "/completions", "/models"):
        if normalized.endswith(suffix):
            normalized = normalized[: -len(suffix)]
            break
    return normalized


def validate_openai_compatible_config(api_key: str, base_url: str, model: str) -> None:
    client = OpenAI(api_key=api_key, base_url=normalize_openai_base_url(base_url))
    try:
        client.models.list()
    except openai.AuthenticationError as exc:
        raise SystemExit(
            "OpenAI authentication failed. Please verify OPENAI_API_KEY is valid for the configured endpoint. "
            f"Details: {exc}"
        ) from exc
    except openai.PermissionDeniedError as exc:
        raise SystemExit(
            "当前网关已拦截这个 key 或模型请求，不是 .env 问题。请更换可用的 OPENAI_BASE_URL / OPENAI_API_KEY，"
            "或确认该网关已放行你填写的 OPENAI_MODEL。"
            f" 详情: {exc}"
        ) from exc
    except openai.NotFoundError as exc:
        raise SystemExit(
            "Model or endpoint not found. Please verify OPENAI_BASE_URL and OPENAI_MODEL. "
            f"Details: {exc}"
        ) from exc
    except openai.RateLimitError as exc:
        raise SystemExit(
            "Rate limit exceeded. Please retry later or reduce request frequency. "
            f"Details: {exc}"
        ) from exc
    except openai.BadRequestError as exc:
        raise SystemExit(
            "Request rejected as invalid by provider. Please check prompt/content policy and model compatibility. "
            f"Details: {exc}"
        ) from exc
    except openai.APIConnectionError as exc:
        raise SystemExit(
            "Failed to connect to OpenAI-compatible endpoint. Please verify OPENAI_BASE_URL and network connectivity. "
            f"Details: {exc}"
        ) from exc


def load_dotenv() -> None:
    env_path = Path(__file__).with_name(".env")
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def build_user_prompt(city: str, preference: str, budget: str) -> str:
    parts = [f"Hello, please help me check today's weather in {city}"]
    if preference or budget:
        extra = []
        if preference:
            extra.append(f"I prefer {preference}")
        if budget:
            extra.append(f"my budget is {budget}")
        parts.append(". " + ", ".join(extra))
    parts.append(", and then recommend a suitable tourist attraction based on the weather.")
    return "".join(parts)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Travel assistant demo from Chapter 1.3")
    parser.add_argument("--city", default="Beijing")
    parser.add_argument("--preference", default="")
    parser.add_argument("--budget", default="")
    parser.add_argument("--max-loops", type=int, default=5)
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()
    api_key = os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("OPENAI_BASE_URL")
    model = os.environ.get("OPENAI_MODEL")

    if not api_key or not base_url or not model:
        raise SystemExit(
            "Please set OPENAI_API_KEY, OPENAI_BASE_URL, and OPENAI_MODEL before running this demo."
        )

    validate_openai_compatible_config(api_key=api_key, base_url=base_url, model=model)

    llm = OpenAICompatibleClient(model=model, api_key=api_key, base_url=base_url)
    agent = TravelAssistantAgent(llm)
    if args.preference or args.budget:
        agent.save_preference(args.preference, args.budget)

    user_prompt = build_user_prompt(args.city, args.preference, args.budget)
    final_answer = agent.run(user_prompt=user_prompt, max_loops=args.max_loops)
    print(f"\nFinal answer:\n{final_answer}")


if __name__ == "__main__":
    main()
