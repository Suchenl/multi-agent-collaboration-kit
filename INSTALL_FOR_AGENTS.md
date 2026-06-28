# INSTALL_FOR_AGENTS.md

This file is written for AI coding agents.

Your task is to adapt a user's repository so it becomes agent-ready without
overwriting their work.

## First Rule

Be conservative. This installer is additive and idempotent. If a file already
exists, preserve it. If a managed section is already present, do not add it again.

## Install Into an Existing Project

If `mackit` is installed:

```bash
mackit adapt /path/to/target-repo --yes
```

From a source checkout of this repository:

```bash
PYTHONPATH=src python -m mackit adapt /path/to/target-repo --yes
```

If the user wants a package skeleton too:

```bash
mackit adapt /path/to/target-repo --package-name your_package_name --yes
```

## Create a Fresh Project

```bash
mackit new /path/to/new-project --package-name your_package_name --yes
```

## Expected Files

After installation, verify these paths exist:

```text
.agents/README.md
.agents/STATE.md
.agents/agents/.gitkeep
.agents/retros/.gitkeep
.agents/skills/.gitkeep
.agents/skills/README.md
.agents/skills/registry.toml
.agents/skills/common/improve-this-kit/SKILL.md
.agents/skills/common/improve-this-kit/reference.md
.agents/tasks/.gitkeep
.agents/improve-this-kit/.gitkeep
.agents/improve-this-kit/README.md
.agents/improve-this-kit/feedback/.gitkeep
.agents/improve-this-kit/feedback/README.md
.agents/improve-this-kit/proposals/.gitkeep
.agents/improve-this-kit/proposals/README.md
.agents/templates/agent_state.md
.agents/templates/feedback.md
.agents/templates/proposal.md
.agents/templates/retro.md
.agents/templates/skill.md
.agents/templates/task_state.md
.cursor/rules/multi-agent.mdc
AGENTS.md
CLAUDE.md
.gitignore
```

By default, optional curated skills from this kit's `.agents/skills/` are also installed into
`.agents/skills/`. Ask the user before narrowing the selection. Use
`--yes` to install all recommended bundles non-interactively,
`--skill-bundles common,graphics` to install specific bundles, or
`--no-curated-skills` to skip optional curated skills.

Recommended agent prompt:

```text
This kit installs curated skill bundles by default: common, workflows, design,
research, and review. Keep all selected unless the user asks to narrow the
installation.
```

External skill discovery is optional. If the user asks for it, follow
`.agents/skills/external/README.md`: report candidate skills first and install
only after approval.

If `--package-name` was provided, also verify:

```text
src/<package_name>/__init__.py
```

## Validation

Run the same install command twice. The second run should report that files
already exist or that managed sections are already present. It must not duplicate
sections in `AGENTS.md`, `CLAUDE.md`, or `.gitignore`.

## Handoff

When done, summarize:

- Which files were created.
- Which files already existed.
- Whether any managed sections were appended.
- Whether the second run was idempotent.

