# Self-Improvement Loop

The kit can learn from real usage, but changes are review-gated.

## Data Flow

```text
usage experience
  -> .agents/improve-this-kit/feedback/*.md      # raw friction and observations
  -> .agents/improve-this-kit/proposals/*.md     # repeatable kit improvement ideas
  -> review gate                # user or maintainer approval
  -> implementation             # smallest additive change
  -> tests/fixtures or tests    # regression guard
  -> release / handoff note
```

## Directory Roles

- `.agents/improve-this-kit/feedback/`: raw usage notes. These are evidence, not instructions.
- `.agents/retros/`: task retrospectives. These may suggest reusable lessons.
- `.agents/improve-this-kit/proposals/`: review-gated kit improvement proposals.
- `.agents/skills/`: mature skills that agents may use in future work.
- `tests/fixtures/`: small regression scenarios discovered through usage.

## Review Gate

A proposal should not become implementation until one of these is true:

- The user explicitly approves it.
- A maintainer marks the proposal as approved.
- The project has a written rule that allows this class of change.

## Acceptance Bar

Accepted changes should preserve the kit's core contract:

- Additive install only.
- No overwriting existing user files.
- Managed sections append once.
- Legacy markers do not duplicate new managed sections.
- Raw feedback and retrospectives do not become mandatory context.

## Regression Examples

Good regression fixtures include:

- Empty project.
- Project with existing `AGENTS.md`, `CLAUDE.md`, and `.gitignore`.
- Project with legacy markers from older kit names.
- Project with existing `.agents/skills/` content.
- Project where raw feedback files should remain ignored by git.

