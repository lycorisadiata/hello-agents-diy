# Error Handling

> How failures are handled in the current Python scripts and Claude hooks.

---

## Overview

This repository does not define a custom exception hierarchy for application code. Current error handling is pragmatic and lightweight:

- helper functions often catch filesystem or parse errors and return fallback values such as `None`, `{}`, `""`, or `False`
- CLI commands print a human-readable error and return a non-zero process code
- hook scripts usually fail open with `sys.exit(0)` so they do not block the Claude session
- warnings for degraded behavior are often printed to stderr instead of raising

This is the pattern to document and follow until the repo adopts stricter error contracts.

---

## Error Types

There are no project-specific error classes in the current codebase.

Instead, modules catch standard library exceptions close to the failure source. Common examples include:

- `FileNotFoundError`, `json.JSONDecodeError`, and `OSError` in `E:/mall/hello-agents-diy/.trellis/scripts/common/io.py`
- `OSError` and `IOError` in `E:/mall/hello-agents-diy/.trellis/scripts/common/paths.py`
- broad `Exception` fallbacks in hook scripts such as `E:/mall/hello-agents-diy/.claude/hooks/session-start.py` and `E:/mall/hello-agents-diy/.claude/hooks/inject-subagent-context.py`

---

## Error Handling Patterns

### Return a fallback instead of raising from low-level helpers

Examples:

- `E:/mall/hello-agents-diy/.trellis/scripts/common/io.py` returns `None` from `read_json` on missing, invalid, or unreadable JSON.
- `E:/mall/hello-agents-diy/.trellis/scripts/common/io.py` returns `False` from `write_json` when writes fail.
- `E:/mall/hello-agents-diy/.trellis/scripts/common/config.py` returns `{}` from `_load_config` when `config.yaml` cannot be read.
- `E:/mall/hello-agents-diy/.trellis/scripts/common/paths.py` returns `None` from `get_developer`, `get_current_task`, and `get_current_task_abs` when state files are missing or invalid.
- `E:/mall/hello-agents-diy/.claude/hooks/statusline.py` returns `""` or `{}` from `_read_text` and `_read_json` when files cannot be read.

### CLI commands surface errors to the user and return an exit code

Examples:

- `E:/mall/hello-agents-diy/.trellis/scripts/task.py` prints colored errors such as `Error: task directory or name required` and returns `1`.
- `E:/mall/hello-agents-diy/.trellis/scripts/common/task_context.py` prints validation problems and returns `1` when context validation fails.
- `E:/mall/hello-agents-diy/.trellis/scripts/add_session.py` prints operational errors to stderr for missing developer or workspace state.

### Hooks usually degrade gracefully and exit 0

Hooks are designed to avoid breaking Claude Code if context injection cannot run.

Examples:

- `E:/mall/hello-agents-diy/.claude/hooks/session-start.py` exits with `sys.exit(0)` when injection should be skipped.
- `E:/mall/hello-agents-diy/.claude/hooks/inject-subagent-context.py` exits with `sys.exit(0)` for malformed input, missing repo root, missing current task, unsupported agent types, or empty context.
- `E:/mall/hello-agents-diy/.claude/hooks/inject-workflow-state.py` returns `0` silently when `.trellis/` or `.current-task` is unavailable.

### Prefer partial behavior over hard failure

Examples:

- `E:/mall/hello-agents-diy/.claude/hooks/session-start.py` uses strings like `No context available` instead of crashing the session-start hook.
- `E:/mall/hello-agents-diy/.claude/hooks/inject-subagent-context.py` warns on stderr when JSONL context is missing, then still lets the sub-agent run with `prd.md` only.
- `E:/mall/hello-agents-diy/.trellis/scripts/common/config.py` falls back to defaults like `DEFAULT_MAX_JOURNAL_LINES` when config values are absent or invalid.

---

## API Error Responses

This repository has no HTTP API layer today, so there is no standard JSON API error envelope.

If future backend HTTP code is added, this spec should be updated after real error response shapes exist in the codebase.

---

## Common Mistakes

- Do not invent exception-heavy patterns that the current codebase does not use.
- Do not let helper-level parse or file errors crash workflows when a fallback return is already the established convention.
- Do not silently swallow user-facing CLI errors without printing a message; command scripts usually explain the problem before returning `1`.
- Do not make Claude hooks fail closed unless blocking behavior is truly intended. Current hooks mostly choose `sys.exit(0)` to preserve the session.

---

## Examples

- Fallback JSON helper: `E:/mall/hello-agents-diy/.trellis/scripts/common/io.py`
- Fallback config loader: `E:/mall/hello-agents-diy/.trellis/scripts/common/config.py`
- CLI exit-code handling: `E:/mall/hello-agents-diy/.trellis/scripts/task.py`
- Hook fail-open behavior: `E:/mall/hello-agents-diy/.claude/hooks/session-start.py`, `E:/mall/hello-agents-diy/.claude/hooks/inject-subagent-context.py`
