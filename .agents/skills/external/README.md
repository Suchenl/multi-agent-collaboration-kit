# External Skill Discovery

Curated skills in `.agents/skills/` can be installed directly from this kit.
External skills are different: agents may discover and recommend them, but should
not install them without user review.

## Discovery Sources

Agents may inspect:

- Existing user skills, such as `~/.cursor/skills/`.
- Existing project skills, such as `.agents/skills/` or `.cursor/skills/`.
- Public repositories that provide `SKILL.md`-style workflows.
- Official framework docs that include agent guides or task workflows.

## Required Review

Before installing an external skill, report:

- Source URL or local path.
- Skill name and trigger description.
- Why it is relevant to the target project.
- Files that would be copied.
- License or attribution notes when visible.

Only install after the user approves the candidate list.

## Installation Rule

Copy approved external skills into `.agents/skills/external/<skill-name>/`.
Do not overwrite existing skills. If a name conflicts, ask the user whether to
rename, skip, or replace.
