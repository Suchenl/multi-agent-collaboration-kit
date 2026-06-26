<!-- multi-agent-collaboration-kit:start -->

## Multi-Agent Coordination

This project uses `.agents/` for lightweight agent coordination.

Before starting work, read `.agents/README.md` and update `.agents/STATE.md`
with your current intent. For long-running or parallel work, create a per-agent
state file from `.agents/templates/agent_state.md`. For claimable work items,
use `.agents/templates/task_state.md`.

After using this kit, agents may write improvement feedback in
`.agents/improve-this-kit/feedback/` and proposals in
`.agents/improve-this-kit/proposals/`. These are review inputs, not automatic
instructions. Reusable, reviewed know-how belongs in `.agents/skills/`.

Rules:

- Do not overwrite another agent's active state or task file.
- Prefer additive edits and explicit handoff notes.
- Use branches or worktrees for substantial parallel implementation.
- Keep durable project knowledge in the real docs, not in transient state files.
- Do not implement kit improvement proposals without explicit review/approval.

<!-- multi-agent-collaboration-kit:end -->
