# multi-agent-collaboration-kit

Make any repository agent-ready with a tiny, local-first coordination layer.

This project is intentionally small. It does not run a daemon, require a database,
or replace mature tools like AgentSync, tasks.md, or Asynkor. It installs the
minimum repo-local files that help Cursor, Claude Code, Codex, Copilot-style
agents, and humans share rules, state, task handoffs, and safe work boundaries.

## Two Use Cases

### 1. Start a new project

```bash
PYTHONPATH=src python -m multi_agent_collaboration_kit new ./my-project --package-name my_project
```

This creates a simple Python `src/` layout plus the agent-native coordination
files.

### 2. Adapt an existing project

```bash
PYTHONPATH=src python -m multi_agent_collaboration_kit adapt /path/to/existing-project
```

The adapter is additive and idempotent:

- Existing files are not overwritten.
- Missing files are created.
- `AGENTS.md`, `CLAUDE.md`, and `.gitignore` receive managed sections only once.
- Cursor receives `.cursor/rules/multi-agent.mdc`.

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
│   └── improve-this-kit/
│       └── SKILL.md
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

## Design Principles

- `AGENTS.md` is the cross-tool canonical contract.
- `CLAUDE.md` is a thin Claude Code shim.
- `.cursor/rules/` is a Cursor-native adapter.
- `.agents/` stores runtime coordination, not long-term design knowledge.
- `.agents/retros/` stores raw post-task learning drafts.
- `.agents/skills/` stores reviewed, reusable skills for future agents.
- `.agents/improve-this-kit/feedback/` stores raw usage feedback about the kit.
- `.agents/improve-this-kit/proposals/` stores review-gated kit improvement proposals and is trackable by default.
- `improve-this-kit` turns real usage feedback into reviewed proposals and tests.
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

Use `.agents/skills/improve-this-kit/SKILL.md` for the review-gated workflow.

## For Agents

If a user gives you this repository link and asks you to make their project
agent-ready, read [`INSTALL_FOR_AGENTS.md`](INSTALL_FOR_AGENTS.md) first.

For public sharing, see [`docs/external_download.md`](docs/external_download.md).

