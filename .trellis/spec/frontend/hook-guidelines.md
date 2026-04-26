# Hook Guidelines

> Current hook conventions in this repository.

---

## Overview

There are no frontend framework hooks such as React custom hooks in this repository today.

Instead, the meaningful "hook" concept here is Claude Code hook scripts under `E:/mall/hello-agents-diy/.claude/hooks/`:

- `session-start.py`
- `inject-subagent-context.py`
- `inject-workflow-state.py`
- `statusline.py`

These are Python executables triggered by the Claude runtime, not frontend hooks.

---

## Current Hook Patterns

### One file per hook responsibility

Examples:

- `E:/mall/hello-agents-diy/.claude/hooks/session-start.py` handles session bootstrap context
- `E:/mall/hello-agents-diy/.claude/hooks/inject-subagent-context.py` handles sub-agent prompt rewriting
- `E:/mall/hello-agents-diy/.claude/hooks/inject-workflow-state.py` handles per-turn workflow breadcrumb injection

### Parse stdin, compute context, print JSON

Examples:

- `E:/mall/hello-agents-diy/.claude/hooks/inject-workflow-state.py` reads JSON from stdin and prints a `hookSpecificOutput` payload
- `E:/mall/hello-agents-diy/.claude/hooks/inject-subagent-context.py` reads tool invocation JSON, rewrites the prompt, and prints updated hook output
- `E:/mall/hello-agents-diy/.claude/hooks/session-start.py` builds structured session context and prints JSON

### Fail open when possible

Hook scripts often return success without output when prerequisites are missing, for example by `sys.exit(0)` or `return 0`.

Examples:

- `E:/mall/hello-agents-diy/.claude/hooks/session-start.py`
- `E:/mall/hello-agents-diy/.claude/hooks/inject-subagent-context.py`
- `E:/mall/hello-agents-diy/.claude/hooks/inject-workflow-state.py`

---

## Data Fetching

There is no browser-side data fetching or frontend hook data layer to describe.

Current hooks read local project files instead:

- `.trellis/.current-task`
- `.trellis/workflow.md`
- task-local `implement.jsonl`, `check.jsonl`, `prd.md`, and `task.json`

Examples are in `E:/mall/hello-agents-diy/.claude/hooks/session-start.py` and `E:/mall/hello-agents-diy/.claude/hooks/inject-subagent-context.py`.

---

## Naming Conventions

- current runtime hook filenames are descriptive and kebab-case, for example `session-start.py` and `inject-workflow-state.py`
- helper function names inside the hook files use snake_case, for example `_parse_hook_input`, `get_research_context`, and `find_trellis_root`

There is no `use*` naming convention because no React hooks exist here yet.

---

## Common Mistakes

- Do not document React hook rules for this repository yet; there are no such files.
- Do not confuse Claude runtime hooks with frontend state hooks.
- Do not make hook output depend on UI framework assumptions; current hooks only depend on stdin JSON, filesystem state, and stdout/stderr.

---

## Guidance for Future Frontend Hooks

If a real frontend app is added later and introduces framework hooks, revise this file using real `use*` examples from that codebase.

---

## Examples

- `E:/mall/hello-agents-diy/.claude/hooks/session-start.py`
- `E:/mall/hello-agents-diy/.claude/hooks/inject-subagent-context.py`
- `E:/mall/hello-agents-diy/.claude/hooks/inject-workflow-state.py`
