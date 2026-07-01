# mackit

[![PyPI version](https://img.shields.io/pypi/v/mackit.svg)](https://pypi.org/project/mackit/)
[![Python versions](https://img.shields.io/pypi/pyversions/mackit.svg)](https://pypi.org/project/mackit/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Make a repository ready for multi-agent work with one clone and one command.

Install from PyPI:

```bash
pip install mackit
```

This kit gives agents a shared workspace (`.agents/`), a small set of
coordination rules, and a curated skill catalog inside `.agents/skills/`. Users do not need to design
their own handoff protocol or hunt for skills before starting: ask an agent to
install this repo, keep the default skill bundles, and start working.

It stays local-first and lightweight. There is no daemon, database, hosted
service, lock server, or required dependency.

It is not trying to replace public skill marketplaces. It complements them by
making a single project immediately usable by agents: install the repo-local
coordination layer, seed a small curated skill set, and add external marketplace
skills only after review.

## Quick Start

```bash
pip install mackit
mackit adapt .
```

When run in a normal terminal, `mackit adapt .` asks whether to install all
optional curated skills, choose specific bundles, or skip optional skills. Press
Enter to accept the recommended default: install all.

```text
Install optional curated skills?
> Yes, install all recommended skills
  No, choose bundles
  Skip optional skills

Select skill bundles:
[x] common
[x] workflows
[x] graphics
[x] research
[x] review
```

For local development from this repository, use `PYTHONPATH=src python -m mackit`.

## Why Pip Install

`mackit` supports two distribution paths:

- `pip install mackit` for normal users who want the fastest path.
- A GitHub checkout for agents and maintainers who need to inspect, adapt, or
  improve the kit.

Pip matters because the main promise of this project is low-friction adoption.
Users should not need to clone this repository, set `PYTHONPATH`, understand the
source layout, or copy files by hand before their project becomes agent-ready.

The installed package includes the CLI, templates, Cursor rule, `.agents/`
coordination files, and optional curated skills. After installation, this should work
from any repository:

```bash
mackit adapt .
```

GitHub remains the source of truth for review, contribution, and agent-readable
implementation details. PyPI is the convenient delivery channel.

## Two Use Cases

### 1. Start a new project

```bash
mackit new ./my-project --package-name my_project
```

This creates a simple Python `src/` layout plus the agent-native coordination
files.

### 2. Adapt an existing project

```bash
mackit adapt /path/to/existing-project
```

The adapter is additive and idempotent:

- Existing files are not overwritten.
- Missing files are created.
- `AGENTS.md`, `CLAUDE.md`, and `.gitignore` receive managed sections only once.
- Cursor receives `.cursor/rules/multi-agent.mdc`.
- Curated skills from this kit's `.agents/skills/` catalog are offered during setup.

## What Gets Installed

```text
.agents/
├── README.md
├── STATE.md
├── agents/.gitkeep
├── retros/.gitkeep
├── skills/
│   ├── .gitkeep
│   ├── README.md
│   ├── registry.toml
│   └── common/
│       └── improve-this-kit/
│           └── SKILL.md
├── tasks/.gitkeep
├── improve-this-kit/
│   ├── .gitkeep
│   ├── README.md
│   ├── feedback/
│   │   ├── .gitkeep
│   │   └── README.md
│   └── proposals/
│       ├── .gitkeep
│       └── README.md
└── templates/
    ├── agent_state.md
    ├── feedback.md
    ├── proposal.md
    ├── retro.md
    ├── skill.md
    └── task_state.md

.cursor/rules/multi-agent.mdc
AGENTS.md
CLAUDE.md
.gitignore
src/<package_name>/        # only for `new`, or when --package-name is passed
```

Selected optional curated skills are copied from this kit's `.agents/skills/` into the
target `.agents/skills/`, preserving grouped paths such as
`graphics/xiaobei-skill-image-to-vba/`.

## Design Principles

- `AGENTS.md` is the cross-tool canonical contract.
- `CLAUDE.md` is a thin Claude Code shim.
- `.cursor/rules/` is a Cursor-native adapter.
- `.agents/` stores runtime coordination, not long-term design knowledge.
- `.agents/agents/*.md` is the source of truth for live per-agent state; `.agents/STATE.md` is only a low-frequency shared summary to avoid parallel write contention.
- State should stay cheap: read only the `STATE.md` top summary by default, keep
  stubs short, and reference logs/paths instead of pasting long output.
- `.agents/retros/` stores raw post-task learning drafts.
- `.agents/skills/` stores reviewed, reusable skills for future agents.
- `.agents/improve-this-kit/feedback/` stores raw usage feedback about the kit.
- `.agents/improve-this-kit/proposals/` stores review-gated kit improvement proposals and is trackable by default.
- `improve-this-kit` turns real usage feedback into reviewed proposals and tests.
- `.agents/skills/registry.toml` describes curated skills and bundles.
- `.agents/skills/external/README.md` tells agents how to recommend external skills safely.
- Design decisions should move to your real docs, ADRs, or README.
- Work isolation should still prefer branches or worktrees for heavy parallelism.

## Self-Improvement Loop

The kit is designed to improve from real usage without letting agents rewrite it
from a single anecdote:

1. Agents write raw usage notes in `.agents/improve-this-kit/feedback/`.
2. Repeatable issues become proposals in `.agents/improve-this-kit/proposals/`.
3. Proposals require explicit review/approval before implementation.
4. Accepted changes must include or update an idempotency check, fixture, or test.
5. Reviewed, reusable know-how can become a skill in `.agents/skills/`.

Use `.agents/skills/common/improve-this-kit/SKILL.md` for the review-gated workflow.

## Curated Skill Catalog

The repo ships its maintained catalog directly in `.agents/skills/`. During
manual terminal use, `mackit` asks whether to install all optional curated
skills, choose specific bundles, or skip them:

```bash
mackit adapt /path/to/project
```

For automation and agents, use explicit flags so the command never waits for
input:

```bash
mackit adapt /path/to/project --yes
mackit adapt /path/to/project --skill-bundles common,graphics
mackit adapt /path/to/project --no-curated-skills
```

Use `list-skill-bundles` to inspect available bundles.

External skill discovery is optional. Agents may recommend external skills, but
must report candidates and wait for user approval before copying them. See
`.agents/skills/external/README.md`.

## For Agents

If a user gives you this repository link and asks you to make their project
agent-ready, read [`INSTALL_FOR_AGENTS.md`](INSTALL_FOR_AGENTS.md) first.

For public sharing, see [`docs/external_download.md`](docs/external_download.md).

