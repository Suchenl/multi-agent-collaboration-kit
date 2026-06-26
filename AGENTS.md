<!-- prepare-agent-cooperation-project:start -->

## Multi-Agent Coordination

This project uses `.agents/` for lightweight agent coordination.

Before starting work, read `.agents/README.md` and update `.agents/STATE.md`
with your current intent. For long-running or parallel work, create a per-agent
state file from `.agents/templates/agent_state.md`. For claimable work items,
use `.agents/templates/task_state.md`.

Rules:

- Do not overwrite another agent's active state or task file.
- Prefer additive edits and explicit handoff notes.
- Use branches or worktrees for substantial parallel implementation.
- Keep durable project knowledge in the real docs, not in transient state files.

<!-- prepare-agent-cooperation-project:end -->
