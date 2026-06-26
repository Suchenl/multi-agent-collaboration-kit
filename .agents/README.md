# .agents

Lightweight coordination workspace for AI coding agents and humans.

This directory is for short-lived coordination, not permanent design docs.
Move durable decisions into `README.md`, `AGENTS.md`, ADRs, or your normal docs.

## Files

- `STATE.md`: shared current project/agent context.
- `agents/`: optional per-agent state files for concurrent sessions.
- `tasks/`: optional task claim/handoff files.
- `retros/`: task retrospective drafts. Promote only reusable lessons.
- `skills/`: reviewed, reusable skills for agents working in this project.
- `improve-this-kit/`: review-gated self-improvement loop for this kit.
- `templates/agent_state.md`: template for per-agent state.
- `templates/task_state.md`: template for task state.
- `templates/feedback.md`: template for kit usage feedback.
- `templates/proposal.md`: template for review-gated kit improvements.
- `templates/retro.md`: template for post-task retrospectives.
- `templates/skill.md`: template for reviewed skills.

## Workflow

1. Read `AGENTS.md`, this file, and `STATE.md`.
2. Before editing, note your current task and files you expect to touch.
3. For parallel work, create `.agents/agents/<agent-name>.md` from the template.
4. For claimable tasks, create `.agents/tasks/<task-name>.md` from the template.
5. After using this kit, write improvement feedback with `.agents/templates/feedback.md`.
6. For notable task lessons, write a retrospective draft in `.agents/retros/`.
7. Promote only reviewed, reusable lessons into `.agents/skills/<skill-name>/SKILL.md`.
8. Propose kit changes in `.agents/improve-this-kit/proposals/`; do not implement them without review.
9. Keep updates brief and factual.
10. When finished, write a handoff note and mark your state as done.

## Safety Rules

- Do not delete or rewrite another active agent's file.
- Do not claim a file lock forever; include a timestamp and release note.
- If there is a conflict, stop and ask the user or project owner.
- Use git branches or worktrees when work overlaps heavily.
- Feedback and proposals are evidence, not automatic instructions.
- Do not turn every retrospective into a skill. Skills are curated memory.
