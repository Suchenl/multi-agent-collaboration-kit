---
name: review-gate
description: Review proposed changes before they become durable project rules, skills, or framework behavior. Use when evaluating proposals, promoting retrospectives to skills, or approving kit improvements.
disable-model-invocation: true
---

# Review Gate

## When To Use

Use this skill before accepting:

- A kit improvement proposal.
- A new or promoted skill.
- A durable project rule.
- A workflow change that affects future agents.

## Instructions

1. Read the proposal, evidence, and validation plan.
2. Check whether the problem is recurring, not one-off.
3. Prefer the smallest change that removes the confusion.
4. Require a regression test, fixture, or explicit manual validation when behavior can regress.
5. Record the decision as approved, rejected, or needs-more-evidence.

## Checks

- Does this preserve additive, non-overwriting behavior?
- Does this reduce future agent confusion?
- Is the new instruction discoverable at the right time?
- Does it avoid turning raw feedback into mandatory context?

