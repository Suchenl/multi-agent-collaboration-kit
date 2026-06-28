---
name: repo-adaptation
description: Adapt an existing repository to use multi-agent-collaboration-kit without overwriting user files. Use when installing the kit, making a repo agent-ready, or validating idempotent setup.
disable-model-invocation: true
---

# Repo Adaptation

## When To Use

Use this skill when adapting an existing project to the kit.

## Instructions

1. Inspect current repo state with git before making changes.
2. Run the kit adapter with the user's selected skill bundles.
3. Run the adapter a second time to verify idempotency.
4. Confirm existing `AGENTS.md`, `CLAUDE.md`, `.gitignore`, and `.agents/` files were preserved.
5. Summarize created files, existing files, appended managed sections, and idempotency result.

## Checks

- The adapter must be additive.
- Managed sections appear once.
- Existing user-authored files are not overwritten.
- Existing skills are preserved.

