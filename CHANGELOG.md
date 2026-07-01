# Changelog

## 0.1.3 - 2026-07-01

- Changed the coordination model to reduce parallel agent write contention:
  `.agents/agents/*.md` is now the source of truth for live per-agent status.
- Reframed `.agents/STATE.md` as a low-frequency shared project summary rather
  than a live task database.
- Updated installed `AGENTS.md`, `.agents/README.md`, `.agents/STATE.md`, and
  `.cursor/rules/multi-agent.mdc` templates to discourage routine
  read-modify-write edits to `.agents/STATE.md`.
- Added token-budget guidance: read only the `STATE.md` top summary by default,
  keep stubs short, keep hook/status messages one line, and reference logs by
  path instead of pasting long output.
- Shortened the default `.agents/templates/agent_state.md` stub.
- Kept package metadata at `0.1.3` per release requirement.
