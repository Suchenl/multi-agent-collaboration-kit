# External Download Guide

Use this repository in one of two ways.

## Install From PyPI

```bash
pip install mackit
mackit adapt /path/to/target-repo
```

## Clone as a New Project Base

```bash
git clone <repo-url> my-project
cd my-project
PYTHONPATH=src python -m mackit new . --package-name my_project
```

After cloning, replace this initializer's README with your project README when
your application starts taking shape.

## Give This Repo to an Agent

In an existing repository, ask your coding agent:

```text
Read <repo-url>/INSTALL_FOR_AGENTS.md and adapt this repository.
Acceptance criteria:
- Create only missing files.
- Do not overwrite existing files.
- Do not duplicate managed sections if the installer is run twice.
```

The agent can then clone this repository to a temporary location and run:

```bash
PYTHONPATH=src python -m mackit adapt /path/to/target-repo --yes
```

The default install includes all curated skill bundles from this kit's
`.agents/skills/` catalog.
Agents should keep the default unless the user asks to narrow the skill set.

## What This Is Not

This is not a central scheduler, lock server, or agent orchestration framework.
It is a small repo-local bootstrap layer. Use worktrees, branches, issue trackers,
or dedicated orchestration tools when coordination becomes complex.

