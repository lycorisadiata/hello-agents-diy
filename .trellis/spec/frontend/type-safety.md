# Type Safety

> Current type-safety conventions relevant to this repository.

---

## Overview

There is no TypeScript code in this repository today.

The repo has no `tsconfig.json`, no `.ts` or `.tsx` files, and no runtime validation library such as Zod or Yup. Do not document TypeScript conventions as if they already exist.

Current type-safety practices are Python-based:

- `from __future__ import annotations` is used broadly, for example in `E:/mall/hello-agents-diy/.trellis/scripts/common/types.py`, `E:/mall/hello-agents-diy/.trellis/scripts/common/config.py`, and `E:/mall/hello-agents-diy/.claude/hooks/session-start.py`
- typed return signatures and unions are used throughout helper modules
- `TypedDict` and frozen dataclasses are used for task metadata in `E:/mall/hello-agents-diy/.trellis/scripts/common/types.py`

---

## Type Organization

Current structured typing lives in Python modules, especially under `.trellis/scripts/common/`.

Examples:

- `E:/mall/hello-agents-diy/.trellis/scripts/common/types.py` defines `TaskData`, `TaskInfo`, and `AgentRecord`
- `E:/mall/hello-agents-diy/.trellis/scripts/common/config.py` annotates config readers like `get_packages(...) -> dict[str, dict] | None`
- `E:/mall/hello-agents-diy/.trellis/scripts/common/paths.py` uses explicit `Path | None` return types for filesystem helpers

---

## Validation

There is no dedicated runtime schema validation framework.

Current validation is lightweight and manual:

- parse JSON and return `{}` or `None` on failure, as in `E:/mall/hello-agents-diy/.claude/hooks/statusline.py` and `E:/mall/hello-agents-diy/.trellis/scripts/common/io.py`
- verify config types with `isinstance`, as in `E:/mall/hello-agents-diy/.trellis/scripts/common/config.py`
- inspect dict keys defensively with `.get(...)`, as in `E:/mall/hello-agents-diy/.claude/hooks/session-start.py` and `E:/mall/hello-agents-diy/.trellis/scripts/task.py`

---

## Common Patterns

- use immutable or narrow public views where useful, for example `@dataclass(frozen=True)` for `TaskInfo`
- use `TypedDict(total=False)` for partially populated serialized records, as in `TaskData` and `AgentRecord`
- keep original raw dicts when writes must preserve unknown fields, as documented by `TaskInfo.raw`
- use explicit union return types for fallback behavior, such as `dict | None`, `str | None`, and `Path | None`

---

## Forbidden Patterns

- Do not invent TypeScript interfaces, React prop types, or Zod schemas that do not exist in this repository.
- Do not claim static frontend type coverage; there is no frontend code to type-check.
- Do not replace defensive file/config parsing with unchecked assumptions about input shape.

---

## Guidance for Future Frontend Code

If the project later adds TypeScript frontend code, rewrite this file around the real compiler settings, shared types, and validation tools that get adopted.

---

## Examples

- `E:/mall/hello-agents-diy/.trellis/scripts/common/types.py`
- `E:/mall/hello-agents-diy/.trellis/scripts/common/config.py`
- `E:/mall/hello-agents-diy/.trellis/scripts/common/paths.py`
- `E:/mall/hello-agents-diy/.claude/hooks/statusline.py`
