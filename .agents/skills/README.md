# .agents/skills

Reviewed, reusable skills for agents working in this project.

Skills are mature operating knowledge, not raw notes. Agents may propose a skill
from a retrospective, but should not promote one without explicit review or a
clear project convention that allows it.

## Layout

```text
<skill-name>/
└── SKILL.md
```

Optional reference files may live beside `SKILL.md`.

## Included Skills

| Skill | Purpose |
|---|---|
| `improve-this-kit/` | Collect feedback and propose review-gated improvements to this kit. |

## Promotion Criteria

- The lesson is likely to apply again.
- The trigger condition is clear.
- The steps are specific and verifiable.
- The skill is concise enough to be worth loading into context.

Use `.agents/templates/skill.md` when creating a new skill.
