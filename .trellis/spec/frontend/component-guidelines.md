# Component Guidelines

> Current guidance for frontend components in this repository.

---

## Overview

No production frontend component code exists in this repository today.

There are no React, Vue, Svelte, or plain browser UI components to model. The only user-facing structured content is Claude markdown configuration plus supporting Python hooks.

Relevant existing files are:

- `E:/mall/hello-agents-diy/.claude/commands/trellis/continue.md`
- `E:/mall/hello-agents-diy/.claude/commands/trellis/finish-work.md`
- `E:/mall/hello-agents-diy/.claude/skills/trellis-before-dev/SKILL.md`
- `E:/mall/hello-agents-diy/.claude/skills/trellis-check/SKILL.md`

---

## Component Structure

Because there are no UI component files, the current reusable authoring pattern is markdown-based instruction files.

Observed patterns:

- command files are single markdown documents with a title, numbered steps, and short code blocks, as in `E:/mall/hello-agents-diy/.claude/commands/trellis/continue.md`
- skill files start with frontmatter and then procedural guidance, as in `E:/mall/hello-agents-diy/.claude/skills/trellis-before-dev/SKILL.md`
- behavior that cannot live in markdown is implemented in nearby Python hook scripts such as `E:/mall/hello-agents-diy/.claude/hooks/session-start.py`

---

## Props Conventions

There are no component props because there are no frontend components.

The nearest equivalent is structured input and output contracts in hook scripts, for example:

- stdin JSON parsing in `E:/mall/hello-agents-diy/.claude/hooks/inject-workflow-state.py`
- prompt payload rewriting in `E:/mall/hello-agents-diy/.claude/hooks/inject-subagent-context.py`

If real UI components are added later, update this section with actual prop typing and composition examples from that code.

---

## Styling Patterns

No frontend styling system exists in this repository today.

There is no CSS, Tailwind, CSS Modules, styled-components, or design system source to document.

---

## Accessibility

There is no shipped browser UI, so there are no current ARIA or semantic HTML conventions to describe.

For the markdown files that do exist, keep headings and ordered steps readable for humans, following examples such as `E:/mall/hello-agents-diy/.claude/commands/trellis/continue.md`.

---

## Common Mistakes

- Do not invent React component patterns for this repo before those files exist.
- Do not describe props, JSX composition, or styling conventions without real examples.
- Do not treat Claude command markdown as if it were browser UI code; it is documentation/configuration, not a frontend runtime.

---

## Examples

- Command document structure: `E:/mall/hello-agents-diy/.claude/commands/trellis/continue.md`
- Skill document structure: `E:/mall/hello-agents-diy/.claude/skills/trellis-before-dev/SKILL.md`
- Runtime support code: `E:/mall/hello-agents-diy/.claude/hooks/inject-subagent-context.py`
