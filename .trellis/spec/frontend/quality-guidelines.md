# Quality Guidelines

> Current quality standards for the frontend layer placeholder in this repository.

---

## Overview

There is no production frontend code in this repository today, so frontend quality guidance must stay narrowly tied to what actually exists:

- Claude command markdown under `E:/mall/hello-agents-diy/.claude/commands/`
- Claude skill markdown under `E:/mall/hello-agents-diy/.claude/skills/`
- supporting Python hook scripts under `E:/mall/hello-agents-diy/.claude/hooks/`

There is no frontend lint setup, no UI test runner, and no browser accessibility test suite.

---

## Forbidden Patterns

- Do not document or enforce React-specific quality rules in this repo yet; there is no React code.
- Do not claim package-manager, TypeScript, or frontend build checks that are not configured.
- Do not add placeholder component, hook, or state conventions that have no concrete code examples.
- Do not let markdown instructions drift away from actual CLI and hook behavior; command and skill docs should match what scripts like `E:/mall/hello-agents-diy/.trellis/scripts/task.py` and `E:/mall/hello-agents-diy/.claude/hooks/session-start.py` really do.

---

## Required Patterns

- keep Claude markdown files readable, with clear headings and ordered steps, following `E:/mall/hello-agents-diy/.claude/commands/trellis/continue.md`
- keep skill docs explicit about workflow steps and command usage, following `E:/mall/hello-agents-diy/.claude/skills/trellis-before-dev/SKILL.md`
- when markdown describes hook or CLI behavior, verify it against the Python implementation
- when editing `.claude/hooks/`, follow the same Python quality expectations documented in backend guidelines: path safety, graceful fallback behavior, and valid JSON output

---

## Testing Requirements

Current repo-accurate checks for this area are:

- read rendered markdown for clarity and consistency after edits
- run targeted Python smoke checks for touched hook scripts
- use `python -m py_compile` on modified hook files to catch syntax errors

There is no frontend lint, typecheck, or component test command to run today.

---

## Code Review Checklist

- Does the change describe only repo-real frontend-adjacent structures such as Claude commands, skills, and hooks?
- If markdown changed, does it still match the current workflow and command behavior?
- If a Claude hook changed, does it still parse stdin safely and emit valid JSON or a deliberate silent exit?
- Are examples pointing to real files such as `E:/mall/hello-agents-diy/.claude/commands/trellis/continue.md` and `E:/mall/hello-agents-diy/.claude/hooks/inject-workflow-state.py`?
- If actual frontend application code is ever added, was this spec updated to reflect that real implementation rather than leaving placeholder text?

---

## Guidance for Future Frontend Code

Once a real frontend app exists, replace this placeholder guidance with actual lint, test, accessibility, and review expectations drawn from that codebase.

---

## Examples

- Command docs: `E:/mall/hello-agents-diy/.claude/commands/trellis/continue.md`, `E:/mall/hello-agents-diy/.claude/commands/trellis/finish-work.md`
- Skill docs: `E:/mall/hello-agents-diy/.claude/skills/trellis-before-dev/SKILL.md`
- Hook code: `E:/mall/hello-agents-diy/.claude/hooks/session-start.py`, `E:/mall/hello-agents-diy/.claude/hooks/inject-workflow-state.py`
