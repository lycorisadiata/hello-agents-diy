# Database Guidelines

> Persistence and data storage conventions for this project today.

---

## Overview

There is no application database layer in this repository today.

- No ORM is present.
- No SQL migrations exist.
- No database client library is configured.
- No tables, models, or repositories exist.

Current persistence is file-based and lightweight:

- JSON files are read and written by helpers in `E:/mall/hello-agents-diy/.trellis/scripts/common/io.py`
- YAML configuration is parsed from `E:/mall/hello-agents-diy/.trellis/config.yaml` by `E:/mall/hello-agents-diy/.trellis/scripts/common/config.py`
- Task state is stored in task-local files such as `E:/mall/hello-agents-diy/.trellis/tasks/00-bootstrap-guidelines/task.json` and `E:/mall/hello-agents-diy/.trellis/tasks/00-bootstrap-guidelines/prd.md`
- Current-session pointers are stored in small control files such as `E:/mall/hello-agents-diy/.trellis/.current-task` and `E:/mall/hello-agents-diy/.trellis/.developer`

---

## Query Patterns

The closest thing to a query layer is direct file access via `pathlib.Path` plus helper wrappers.

### JSON access goes through shared helpers when possible

Examples:

- `E:/mall/hello-agents-diy/.trellis/scripts/common/io.py` provides `read_json(path: Path) -> dict | None`.
- `E:/mall/hello-agents-diy/.trellis/scripts/task.py` uses `read_json` and `write_json` for task.json updates.
- `E:/mall/hello-agents-diy/.trellis/scripts/common/task_context.py` reads JSONL context files line by line with `json.loads`.

### YAML access is custom and dependency-free

Examples:

- `E:/mall/hello-agents-diy/.trellis/scripts/common/config.py` parses `.trellis/config.yaml` with `parse_simple_yaml` instead of bringing in PyYAML.
- Config readers such as `get_packages`, `get_default_package`, and `get_spec_scope` layer typed access on top of the raw parsed dict.

### Path-based lookup is normal

Examples:

- `E:/mall/hello-agents-diy/.trellis/scripts/common/paths.py` resolves task refs to file paths.
- `E:/mall/hello-agents-diy/.claude/hooks/inject-subagent-context.py` reads files and directories listed in task JSONL manifests.
- `E:/mall/hello-agents-diy/.claude/hooks/statusline.py` reads `.trellis/.current-task` and nearby `task.json` files directly.

---

## Migrations

There is no migration system.

When data shapes change, current code usually handles it by:

- using permissive dict access such as `data.get(...)`
- allowing missing fields in `TypedDict(total=False)` definitions, as in `E:/mall/hello-agents-diy/.trellis/scripts/common/types.py`
- preserving original task dicts for write-back, as documented in `TaskData` and `TaskInfo.raw`

That means compatibility is currently maintained in code, not through versioned database migrations.

---

## Naming Conventions

Since there are no database tables or columns, naming guidance applies to files and serialized keys instead.

- JSON and YAML keys are lowercase with underscores when newly introduced, for example `base_branch`, `worktree_path`, and `session_commit_message`.
- Task metadata keys in `task.json` are stable string fields documented in `E:/mall/hello-agents-diy/.trellis/scripts/common/types.py`.
- Control files use dot-prefixed names under `.trellis/`, for example `.current-task` and `.developer`.

---

## Common Mistakes to Avoid

- Do not invent ORM, migration, or transaction conventions in this spec; none exist in the repo.
- Do not replace existing file-based persistence with a database abstraction unless the repository actually adopts one.
- Do not assume `read_json` raises on bad input. In `E:/mall/hello-agents-diy/.trellis/scripts/common/io.py` it returns `None` for missing or invalid files, so callers should handle that fallback path.
- Do not drop unknown task fields during rewrites; `E:/mall/hello-agents-diy/.trellis/scripts/common/types.py` explicitly says writes should preserve the original dict.

---

## Examples

- JSON helper layer: `E:/mall/hello-agents-diy/.trellis/scripts/common/io.py`
- YAML config parser: `E:/mall/hello-agents-diy/.trellis/scripts/common/config.py`
- Task metadata shape: `E:/mall/hello-agents-diy/.trellis/scripts/common/types.py`
- Task lifecycle state file: `E:/mall/hello-agents-diy/.trellis/tasks/00-bootstrap-guidelines/task.json`
- Repo config source: `E:/mall/hello-agents-diy/.trellis/config.yaml`
