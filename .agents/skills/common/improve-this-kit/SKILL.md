---
name: improve-this-kit
description: Collect review-gated feedback and improvement proposals for multi-agent-collaboration-kit. Use after adapting a project with this kit, when an agent reports friction using .agents/, or when the user asks how to improve the collaboration framework.
disable-model-invocation: true
---

# Improve This Kit

## Purpose

Turn real usage into reviewed improvements without letting agents rewrite the
framework from a single anecdote.

## When To Use

Use this skill after:

- Installing or adapting a project with `multi-agent-collaboration-kit`.
- Completing a multi-agent workflow that used `.agents/`.
- Finding confusing, missing, or noisy coordination instructions.
- The user asks for feedback on this kit or how to improve it.

## Workflow

1. Write usage feedback in `.agents/improve-this-kit/feedback/<date>-<short-name>.md` using `.agents/templates/feedback.md`.
2. If the feedback reveals a repeatable issue, write a proposal in `.agents/improve-this-kit/proposals/<short-name>.md` using `.agents/templates/proposal.md`.
3. Do not edit the kit from feedback alone. Wait for explicit user approval or an existing project rule that allows the change.
4. When approved, make the smallest change that addresses the proposal.
5. Add or update an idempotency check, fixture, or test that would fail if the issue returns.
6. Record the result in the proposal's review notes.

## Proposal Quality Bar

A proposal is worth implementing only if:

- The pain is likely to recur across projects or agents.
- The expected behavior is easy to verify.
- The fix is smaller than the confusion it removes.
- It preserves the additive, non-overwriting install contract.

## Anti-Patterns

- Do not promote every complaint into a framework change.
- Do not convert raw feedback directly into a skill.
- Do not add orchestration, daemons, lock servers, or external dependencies unless the user explicitly asks.
- Do not change installed project files destructively to match the latest kit.

## Reference

For the full feedback -> proposal -> review -> implementation loop, read
`reference.md`.
