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
├── tasks/.gitkeep
└── templates/
    ├── agent_state.md
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
- Design decisions should move to your real docs, ADRs, or README.
- Work isolation should still prefer branches or worktrees for heavy parallelism.

## For Agents

If a user gives you this repository link and asks you to make their project
agent-ready, read [`INSTALL_FOR_AGENTS.md`](INSTALL_FOR_AGENTS.md) first.

For public sharing, see [`docs/external_download.md`](docs/external_download.md).

