# Quality Guidelines

> Code quality standards for the current Python scripts and Claude hooks.

---

## Overview

This repository currently consists of workflow automation scripts, task metadata helpers, and Claude hook integrations. Quality review should focus on correctness, portability, and failure behavior for those scripts rather than generic web-backend concerns.

There is no `pyproject.toml`, no `requirements.txt`, no dedicated test suite, and no repo-local lint configuration at the moment. Verification is therefore lightweight and should stay factual.

---

## Forbidden Patterns

- Do not invent backend frameworks, request handlers, or service abstractions that are not present in this repository.
- Do not break the fail-open hook contract by turning routine context-miss cases into hard failures. Current hook scripts usually exit `0` when they cannot inject context.
- Do not duplicate path, config, or JSON handling logic across entry points when helpers already exist in `E:/mall/hello-agents-diy/.trellis/scripts/common/`.
- Do not rewrite `task.json` through narrow typed objects that discard unknown keys; `E:/mall/hello-agents-diy/.trellis/scripts/common/types.py` explicitly preserves raw dicts for write-back.
- Do not assume Unix-only behavior. Existing code contains Windows encoding guards and path normalization in files such as `E:/mall/hello-agents-diy/.claude/hooks/session-start.py`, `E:/mall/hello-agents-diy/.claude/hooks/statusline.py`, and `E:/mall/hello-agents-diy/.trellis/scripts/common/paths.py`.

---

## Required Patterns

- Prefer `pathlib.Path` and shared path helpers, following `E:/mall/hello-agents-diy/.trellis/scripts/common/paths.py`.
- Prefer small, reusable helper functions for parsing and filesystem behavior, following `E:/mall/hello-agents-diy/.trellis/scripts/common/io.py` and `E:/mall/hello-agents-diy/.trellis/scripts/common/config.py`.
- Keep CLI entry points readable and shallow, as in `E:/mall/hello-agents-diy/.trellis/scripts/task.py`, with real work delegated to `common/` modules.
- Preserve graceful fallback returns for file and config reads unless the command truly cannot continue.
- When touching hook scripts, verify stdin/stdout JSON contract and silent-exit behavior still match how Claude hooks are currently implemented.

---

## Testing Requirements

Current repo-accurate verification means:

- run the relevant Python command directly when you change a CLI script, for example `python ./.trellis/scripts/task.py --help`
- run the affected hook script in a way that at least validates it starts and parses, or use a Python compile pass across modified scripts
- when a change affects file parsing, current-task resolution, or task metadata, exercise the real command path that uses it

Because there is no configured lint or typecheck command in this repository, do not claim framework-specific linting or mypy coverage that does not exist.

Practical checks for this repo are:

- `python -m py_compile` over touched Python files
- `python ./.trellis/scripts/task.py --help`
- other targeted command smoke tests when relevant

---

## Code Review Checklist

- Does the change match the current repo shape: Python scripts plus Claude hooks, not a hypothetical app backend?
- Does it reuse existing helpers from `E:/mall/hello-agents-diy/.trellis/scripts/common/` where appropriate?
- Are path handling and encoding behavior still safe on Windows, as existing scripts expect?
- If a file read, JSON parse, or config lookup fails, does behavior degrade the same way nearby code already does?
- If `task.json` or JSONL files are modified, are unknown fields and seed rows handled safely?
- If output changed, is it still understandable for terminal users and consistent with `log_*` helpers or existing print style?
- If a hook changed, does it still return valid JSON output or a silent success exit where expected?

---

## Examples

- Shared helper quality patterns: `E:/mall/hello-agents-diy/.trellis/scripts/common/io.py`, `E:/mall/hello-agents-diy/.trellis/scripts/common/config.py`, `E:/mall/hello-agents-diy/.trellis/scripts/common/paths.py`
- Typed task metadata without lossy writes: `E:/mall/hello-agents-diy/.trellis/scripts/common/types.py`
- Thin CLI orchestration: `E:/mall/hello-agents-diy/.trellis/scripts/task.py`
- Hook robustness and Windows support: `E:/mall/hello-agents-diy/.claude/hooks/session-start.py`, `E:/mall/hello-agents-diy/.claude/hooks/inject-subagent-context.py`, `E:/mall/hello-agents-diy/.claude/hooks/statusline.py`
