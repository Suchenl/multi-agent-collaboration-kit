# INSTALL_FOR_AGENTS.md

This file is written for AI coding agents.

Your task is to adapt a user's repository so it becomes agent-ready without
overwriting their work.

## First Rule

Be conservative. This installer is additive and idempotent. If a file already
exists, preserve it. If a managed section is already present, do not add it again.

## Install Into an Existing Project

From this repository:

```bash
PYTHONPATH=src python -m multi_agent_collaboration_kit adapt /path/to/target-repo
```

If the user wants a package skeleton too:

```bash
PYTHONPATH=src python -m multi_agent_collaboration_kit adapt /path/to/target-repo --package-name your_package_name
```

## Create a Fresh Project

```bash
PYTHONPATH=src python -m multi_agent_collaboration_kit new /path/to/new-project --package-name your_package_name
```

## Expected Files

After installation, verify these paths exist:

```text
.agents/README.md
.agents/STATE.md
.agents/agents/.gitkeep
.agents/tasks/.gitkeep
.agents/templates/agent_state.md
.agents/templates/task_state.md
.cursor/rules/multi-agent.mdc
AGENTS.md
CLAUDE.md
.gitignore
```

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

