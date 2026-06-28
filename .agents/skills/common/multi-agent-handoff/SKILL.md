---
name: multi-agent-handoff
description: Maintain clear state and handoff notes across multiple AI agents or human-agent sessions. Use when work spans multiple agents, parallel sessions, handoffs, or potentially overlapping file edits.
disable-model-invocation: true
---

# Multi-Agent Handoff

## When To Use

Use this skill when:

- Multiple agents may work in the same repository.
- A task is paused, handed off, or resumed later.
- File edits may overlap.
- The user asks for status or continuation across sessions.

## Instructions

1. Read `AGENTS.md`, `.agents/README.md`, and `.agents/STATE.md`.
2. Record your active intent in `.agents/STATE.md` or a per-agent file under `.agents/agents/`.
3. For claimable work, create or update a task file under `.agents/tasks/`.
4. List files you expect to touch before editing.
5. At handoff, summarize result, touched files, blockers, and next action.

## Checks

- Do not overwrite another active agent's state file.
- Use branches or worktrees for heavy overlapping implementation.
- Keep durable project knowledge in real docs, not transient state.

