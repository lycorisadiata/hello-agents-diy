# Directory Structure

> How backend code is organized in this project today.

---

## Overview

This repository does not contain a web backend, API server, or service layer yet. The only production code is Python automation for the Trellis workflow plus Claude hook scripts. Document backend changes against that reality.

The main code areas are:

- `.trellis/scripts/` for user-facing CLI entry points such as `E:/mall/hello-agents-diy/.trellis/scripts/task.py` and `E:/mall/hello-agents-diy/.trellis/scripts/get_context.py`
- `.trellis/scripts/common/` for reusable helpers such as `E:/mall/hello-agents-diy/.trellis/scripts/common/paths.py`, `E:/mall/hello-agents-diy/.trellis/scripts/common/config.py`, and `E:/mall/hello-agents-diy/.trellis/scripts/common/log.py`
- `.trellis/scripts/hooks/` for workflow integrations such as `E:/mall/hello-agents-diy/.trellis/scripts/hooks/linear_sync.py`
- `.claude/hooks/` for Claude runtime hook scripts such as `E:/mall/hello-agents-diy/.claude/hooks/session-start.py` and `E:/mall/hello-agents-diy/.claude/hooks/inject-subagent-context.py`

---

## Directory Layout

```text
E:/mall/hello-agents-diy/
├── .trellis/
│   ├── config.yaml
│   ├── workflow.md
│   ├── scripts/
│   │   ├── task.py
│   │   ├── get_context.py
│   │   ├── add_session.py
│   │   └── common/
│   │       ├── paths.py
│   │       ├── config.py
│   │       ├── io.py
│   │       ├── log.py
│   │       ├── task_context.py
│   │       └── types.py
│   └── tasks/
└── .claude/
    ├── hooks/
    │   ├── session-start.py
    │   ├── inject-subagent-context.py
    │   ├── inject-workflow-state.py
    │   └── statusline.py
    ├── commands/
    └── skills/
```

---

## Module Organization

### CLI entry points stay shallow

Top-level scripts under `.trellis/scripts/` are thin command entry points that delegate to shared helpers.

Examples:

- `E:/mall/hello-agents-diy/.trellis/scripts/task.py` wires argparse subcommands and imports handlers from `common.task_store` and `common.task_context`.
- `E:/mall/hello-agents-diy/.trellis/scripts/get_context.py` is a top-level executable rather than being buried in a feature subpackage.
- `E:/mall/hello-agents-diy/.trellis/scripts/init_developer.py` is another standalone workflow command.

### Shared logic goes in `common/`

Cross-script behavior is centralized in `.trellis/scripts/common/` instead of duplicated across entry points.

Examples:

- Path and repo discovery logic lives in `E:/mall/hello-agents-diy/.trellis/scripts/common/paths.py`.
- YAML config parsing lives in `E:/mall/hello-agents-diy/.trellis/scripts/common/config.py`.
- JSON file helpers live in `E:/mall/hello-agents-diy/.trellis/scripts/common/io.py`.
- Typed task models live in `E:/mall/hello-agents-diy/.trellis/scripts/common/types.py`.

### Claude runtime integrations live under `.claude/hooks/`

Hook scripts are kept separate from `.trellis/scripts/` because they are executed by Claude Code, not by the Trellis CLI.

Examples:

- `E:/mall/hello-agents-diy/.claude/hooks/session-start.py` injects workflow context.
- `E:/mall/hello-agents-diy/.claude/hooks/inject-subagent-context.py` rewrites sub-agent prompts.
- `E:/mall/hello-agents-diy/.claude/hooks/statusline.py` renders status line output.

---

## Naming Conventions

- Python modules use snake_case filenames: `task_context.py`, `git_context.py`, `session-start.py`.
- CLI entry points are named for the command they expose: `task.py`, `get_context.py`, `init_developer.py`.
- Shared constants are uppercase, often grouped near the top of the file, for example `DIR_WORKFLOW`, `DIR_TASKS`, and `FILE_CURRENT_TASK` in `E:/mall/hello-agents-diy/.trellis/scripts/common/paths.py`.
- Reusable data containers use descriptive nouns such as `TaskInfo`, `TaskData`, and `AgentRecord` in `E:/mall/hello-agents-diy/.trellis/scripts/common/types.py`.

---

## Current Anti-Patterns to Avoid

- Do not document imaginary `src/`, `routes/`, `services/`, or `controllers/` directories for this repo. They do not exist today.
- Do not add large amounts of business logic directly into multiple CLI scripts when a shared helper under `.trellis/scripts/common/` would keep behavior consistent.
- Do not mix Claude hook runtime code into `.trellis/scripts/common/`; hook scripts have different entry points and I/O contracts.

---

## Examples

- CLI plus shared helper split: `E:/mall/hello-agents-diy/.trellis/scripts/task.py` with `E:/mall/hello-agents-diy/.trellis/scripts/common/task_context.py`
- File-system utility module: `E:/mall/hello-agents-diy/.trellis/scripts/common/paths.py`
- Config and persistence helpers: `E:/mall/hello-agents-diy/.trellis/scripts/common/config.py`, `E:/mall/hello-agents-diy/.trellis/scripts/common/io.py`
- Claude integration scripts: `E:/mall/hello-agents-diy/.claude/hooks/session-start.py`, `E:/mall/hello-agents-diy/.claude/hooks/inject-workflow-state.py`
