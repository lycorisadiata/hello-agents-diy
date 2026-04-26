# Logging Guidelines

> How output and operational logging work in this repository today.

---

## Overview

There is no stdlib `logging` configuration in this codebase today.

Current scripts use a mix of:

- shared `log_*` helper functions from `E:/mall/hello-agents-diy/.trellis/scripts/common/log.py`
- direct `print(...)` for user-facing CLI output
- direct `print(..., file=sys.stderr)` for warnings and operational notices in hooks and utility scripts

That is the real convention to document. Do not describe handlers, formatters, or logging config files that do not exist.

---

## Log Levels

### Shared helper levels in CLI code

`E:/mall/hello-agents-diy/.trellis/scripts/common/log.py` defines four prefixed helpers:

- `log_info` → `[INFO]`
- `log_success` → `[SUCCESS]`
- `log_warn` → `[WARN]`
- `log_error` → `[ERROR]`

Use these when you want consistent colored terminal status output across Trellis scripts.

### Plain `print` is also common

Examples:

- `E:/mall/hello-agents-diy/.trellis/scripts/task.py` prints usage text and task summaries directly.
- `E:/mall/hello-agents-diy/.trellis/scripts/common/task_context.py` prints section headers and validation results directly.
- `E:/mall/hello-agents-diy/.claude/hooks/statusline.py` prints the final status line payload directly.

### Hook warnings go to stderr

Examples:

- `E:/mall/hello-agents-diy/.claude/hooks/inject-subagent-context.py` prints WARN messages to `sys.stderr` when JSONL context files are missing or empty.
- `E:/mall/hello-agents-diy/.claude/hooks/session-start.py` prints scope and package warnings to `sys.stderr`.
- `E:/mall/hello-agents-diy/.trellis/scripts/add_session.py` prints git auto-commit warnings to `sys.stderr`.

---

## Structured Logging

There is no structured JSON logging setup.

The closest thing to a standard format is the prefixed terminal output from `E:/mall/hello-agents-diy/.trellis/scripts/common/log.py`, plus consistent textual warnings such as:

- `[inject-subagent-context] WARN: ...`
- `Warning: ...`
- `Error: ...`

Keep output readable for humans in a terminal session. Current code optimizes for developer-facing CLI clarity, not machine-ingested log pipelines.

---

## What to Log

- user-relevant command outcomes, for example success or failure to set the current task in `E:/mall/hello-agents-diy/.trellis/scripts/task.py`
- degraded behavior that should be visible but not fatal, for example missing JSONL context in `E:/mall/hello-agents-diy/.claude/hooks/inject-subagent-context.py`
- warnings about invalid config or package scope, as in `E:/mall/hello-agents-diy/.trellis/scripts/common/config.py` and `E:/mall/hello-agents-diy/.claude/hooks/session-start.py`
- lifecycle progress in longer scripts, as in `E:/mall/hello-agents-diy/.trellis/scripts/add_session.py`

---

## What NOT to Log

- do not add fake structured fields, request IDs, or service metadata that the repo does not use today
- do not log full file contents when a short status message is enough
- avoid secrets if future config grows to include them; current `.trellis/config.yaml` only contains workflow settings, but the repo should still treat config values conservatively
- avoid noisy debug output in hooks unless it is necessary for diagnosing a hook-specific failure path

---

## Examples

- Shared colored log helpers: `E:/mall/hello-agents-diy/.trellis/scripts/common/log.py`
- CLI output-heavy command: `E:/mall/hello-agents-diy/.trellis/scripts/task.py`
- Stderr warning style in hooks: `E:/mall/hello-agents-diy/.claude/hooks/inject-subagent-context.py`
- Stderr operational notices: `E:/mall/hello-agents-diy/.trellis/scripts/add_session.py`
