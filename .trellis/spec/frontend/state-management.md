# State Management

> Current state-management reality for this repository.

---

## Overview

There is no frontend state library in this repository today because there is no frontend application code.

No Redux, Zustand, React Context, MobX, URL router state, or server-state library is present.

The main persistent state that does exist is file-based workflow state for Trellis and Claude hooks.

Examples:

- active task pointer in `E:/mall/hello-agents-diy/.trellis/.current-task`
- developer identity in `E:/mall/hello-agents-diy/.trellis/.developer`
- task metadata in `E:/mall/hello-agents-diy/.trellis/tasks/00-bootstrap-guidelines/task.json`
- workflow config in `E:/mall/hello-agents-diy/.trellis/config.yaml`

---

## State Categories

### Persistent file state

This is the dominant state model in the repo.

- JSON task data is handled by `E:/mall/hello-agents-diy/.trellis/scripts/common/io.py`
- YAML config is parsed by `E:/mall/hello-agents-diy/.trellis/scripts/common/config.py`
- task and workspace paths are resolved by `E:/mall/hello-agents-diy/.trellis/scripts/common/paths.py`

### In-process derived state

Scripts compute small derived values in memory while running, then discard them.

Examples:

- package scope resolution in `E:/mall/hello-agents-diy/.claude/hooks/session-start.py`
- active task summaries in `E:/mall/hello-agents-diy/.claude/hooks/statusline.py`
- JSONL validation counters in `E:/mall/hello-agents-diy/.trellis/scripts/common/task_context.py`

There is no long-lived client-side state container.

---

## When to Use Global State

There is no frontend global state concept today.

For current Python tooling, shared state belongs in files under `.trellis/` when it must persist across commands or sessions. Otherwise, keep it local to the running script.

Examples:

- persisted cross-session state: `.trellis/.current-task`, `.trellis/.developer`
- per-run temporary state: local variables inside `E:/mall/hello-agents-diy/.claude/hooks/inject-subagent-context.py`

---

## Server State

There is no server-state cache or HTTP data synchronization layer.

Current scripts read local files directly each run rather than caching remote data.

---

## Common Mistakes

- Do not invent frontend state architecture for this repository before frontend code exists.
- Do not describe browser local state versus global state patterns that are not implemented anywhere.
- Do not move simple persisted workflow state out of `.trellis/` files without a real repository-wide design change.

---

## Guidance for Future Frontend Code

If a UI app is added later, replace this file with actual state boundaries from that codebase and include concrete examples from real frontend modules.

---

## Examples

- File-backed state helpers: `E:/mall/hello-agents-diy/.trellis/scripts/common/io.py`, `E:/mall/hello-agents-diy/.trellis/scripts/common/config.py`, `E:/mall/hello-agents-diy/.trellis/scripts/common/paths.py`
- Hook-derived status view: `E:/mall/hello-agents-diy/.claude/hooks/statusline.py`
