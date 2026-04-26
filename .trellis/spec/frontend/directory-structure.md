# Directory Structure

> Current frontend-related structure in this repository.

---

## Overview

There is no production frontend application in this repository today.

The repo has no:

- `src/` frontend directory
- `package.json`
- `tsconfig.json`
- `.ts`, `.tsx`, `.js`, or `.jsx` application source files

So this spec should not describe React pages, components, routes, assets, or feature folders that do not exist.

The closest frontend-adjacent structure is Claude-facing markdown and hook infrastructure:

- `E:/mall/hello-agents-diy/.claude/commands/` contains command docs such as `E:/mall/hello-agents-diy/.claude/commands/trellis/continue.md`
- `E:/mall/hello-agents-diy/.claude/skills/` contains skill markdown such as `E:/mall/hello-agents-diy/.claude/skills/trellis-before-dev/SKILL.md`
- `E:/mall/hello-agents-diy/.claude/hooks/` contains Python hook scripts that support the Claude runtime

---

## Directory Layout

```text
E:/mall/hello-agents-diy/.claude/
├── agents/
├── commands/
│   └── trellis/
│       ├── continue.md
│       └── finish-work.md
├── hooks/
│   ├── session-start.py
│   ├── inject-subagent-context.py
│   ├── inject-workflow-state.py
│   └── statusline.py
└── skills/
    ├── trellis-before-dev/
    │   └── SKILL.md
    ├── trellis-brainstorm/
    │   └── SKILL.md
    └── trellis-check/
        └── SKILL.md
```

---

## Module Organization

For the structures that do exist today:

- one Claude command lives in one markdown file under `.claude/commands/...`
- one Claude skill lives in its own directory with `SKILL.md`
- runtime automation for Claude lives in Python files under `.claude/hooks/`

Examples:

- Command doc: `E:/mall/hello-agents-diy/.claude/commands/trellis/continue.md`
- Skill doc: `E:/mall/hello-agents-diy/.claude/skills/trellis-before-dev/SKILL.md`
- Hook implementation: `E:/mall/hello-agents-diy/.claude/hooks/session-start.py`

---

## Naming Conventions

- command docs are lowercase markdown files, for example `continue.md` and `finish-work.md`
- skill folders use kebab-case names such as `trellis-before-dev` and `trellis-update-spec`
- each skill directory uses a single uppercase `SKILL.md` file
- hook scripts use descriptive filenames tied to the hook purpose, for example `inject-workflow-state.py`

---

## Guidance for Future Frontend Code

When a real frontend app is added, update this file with actual directory layout from that codebase. Until then, do not invent a component or page structure here.

---

## Examples

- `E:/mall/hello-agents-diy/.claude/commands/trellis/continue.md`
- `E:/mall/hello-agents-diy/.claude/skills/trellis-before-dev/SKILL.md`
- `E:/mall/hello-agents-diy/.claude/hooks/session-start.py`
