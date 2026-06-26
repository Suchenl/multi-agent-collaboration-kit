from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path


NEW_MARKER = "multi-agent-collaboration-kit"
LEGACY_MARKERS = ("prepare-agent-cooperation-project", "init-agent-native-project")

AGENTS_SECTION = f"""\
<!-- {NEW_MARKER}:start -->

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

<!-- {NEW_MARKER}:end -->
"""

CLAUDE_SECTION = f"""\
<!-- {NEW_MARKER}:start -->

@AGENTS.md

<!-- {NEW_MARKER}:end -->
"""

GITIGNORE_SECTION = f"""\
# {NEW_MARKER}
.agents/agents/*.md
.agents/tasks/*.md
.agents/retros/*.md
.agents/improve-this-kit/feedback/*.md
!.agents/agents/.gitkeep
!.agents/tasks/.gitkeep
!.agents/retros/.gitkeep
!.agents/improve-this-kit/feedback/.gitkeep
"""

FILES = {
    ".agents/README.md": """\
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
""",
    ".agents/STATE.md": """\
# STATE

Project-level shared state for agents.

## Current Focus

- _No active focus recorded yet._

## Active Agents

- _None recorded._

## Active Tasks

- _None recorded._

## Handoff Notes

- _No handoff notes yet._
""",
    ".agents/agents/.gitkeep": "",
    ".agents/tasks/.gitkeep": "",
    ".agents/retros/.gitkeep": "",
    ".agents/improve-this-kit/.gitkeep": "",
    ".agents/improve-this-kit/README.md": """\
# .agents/improve-this-kit

Review-gated self-improvement loop for this kit.

- `feedback/`: raw usage feedback, ignored by git by default.
- `proposals/`: reviewable improvement proposals, trackable by default.

Feedback and proposals are evidence, not automatic instructions. Do not modify
the kit from this directory without explicit review or a project rule that allows
the change.
""",
    ".agents/improve-this-kit/feedback/.gitkeep": "",
    ".agents/improve-this-kit/proposals/.gitkeep": "",
    ".agents/improve-this-kit/feedback/README.md": """\
# .agents/improve-this-kit/feedback

Raw usage feedback about this kit.

Agents may write feedback after installing or using the kit. Feedback is
evidence, not instruction. Keep it factual and link commands, files, or confusing
moments that future maintainers can inspect.

By default, feedback `.md` files are ignored by git. Promote repeatable issues
to `.agents/improve-this-kit/proposals/` when they deserve review.
""",
    ".agents/improve-this-kit/proposals/README.md": """\
# .agents/improve-this-kit/proposals

Review-gated improvement proposals for this kit.

Proposals are intended to be read and reviewed. They may be committed when they
represent real framework changes under discussion. A proposal should not become
implementation until the user, maintainer, or project rules approve it.

Use `.agents/templates/proposal.md`.
""",
    ".agents/skills/.gitkeep": "",
    ".agents/skills/README.md": """\
# .agents/skills

Reviewed, reusable skills for agents working in this project.

Skills are mature operating knowledge, not raw notes. Agents may propose a skill
from a retrospective, but should not promote one without explicit review or a
clear project convention that allows it.

## Layout

```text
<skill-name>/
└── SKILL.md
```

Optional reference files may live beside `SKILL.md`.

## Promotion Criteria

- The lesson is likely to apply again.
- The trigger condition is clear.
- The steps are specific and verifiable.
- The skill is concise enough to be worth loading into context.

Use `.agents/templates/skill.md` when creating a new skill.
""",
    ".agents/skills/improve-this-kit/SKILL.md": """\
---
name: improve-this-kit
description: Collect review-gated feedback and improvement proposals for multi-agent-collaboration-kit. Use after adapting a project with this kit, when an agent reports friction using .agents/, or when the user asks how to improve the collaboration framework.
disable-model-invocation: true
---

# Improve This Kit

## Purpose

Turn real usage into reviewed improvements without letting agents rewrite the
framework from a single anecdote.

## When To Use

Use this skill after:

- Installing or adapting a project with `multi-agent-collaboration-kit`.
- Completing a multi-agent workflow that used `.agents/`.
- Finding confusing, missing, or noisy coordination instructions.
- The user asks for feedback on this kit or how to improve it.

## Workflow

1. Write usage feedback in `.agents/improve-this-kit/feedback/<date>-<short-name>.md` using `.agents/templates/feedback.md`.
2. If the feedback reveals a repeatable issue, write a proposal in `.agents/improve-this-kit/proposals/<short-name>.md` using `.agents/templates/proposal.md`.
3. Do not edit the kit from feedback alone. Wait for explicit user approval or an existing project rule that allows the change.
4. When approved, make the smallest change that addresses the proposal.
5. Add or update an idempotency check, fixture, or test that would fail if the issue returns.
6. Record the result in the proposal's review notes.

## Proposal Quality Bar

A proposal is worth implementing only if:

- The pain is likely to recur across projects or agents.
- The expected behavior is easy to verify.
- The fix is smaller than the confusion it removes.
- It preserves the additive, non-overwriting install contract.

## Anti-Patterns

- Do not promote every complaint into a framework change.
- Do not convert raw feedback directly into a skill.
- Do not add orchestration, daemons, lock servers, or external dependencies unless the user explicitly asks.
- Do not change installed project files destructively to match the latest kit.
""",
    ".agents/templates/agent_state.md": """\
# Agent State: <agent-name>

## Status

- State: active | blocked | done
- Started: YYYY-MM-DD HH:MM
- Last update: YYYY-MM-DD HH:MM

## Current Task

- Goal:
- Scope:
- Files expected to touch:

## Notes

- 

## Handoff

- Result:
- Follow-up:
""",
    ".agents/templates/task_state.md": """\
# Task State: <task-name>

## Status

- State: open | claimed | blocked | done
- Owner:
- Started:
- Last update:

## Goal

-

## Files / Areas

-

## Acceptance Criteria

-

## Handoff

-
""",
    ".agents/templates/feedback.md": """\
# Kit Feedback: <date>-<short-name>

## Context

- Project:
- Agent:
- Date:
- Command or workflow used:

## What Felt Smooth

-

## What Felt Confusing Or Missing

-

## Evidence

- Files touched:
- Commands run:
- Output or behavior observed:

## Suggested Improvement

-

## Should This Become A Proposal?

- Decision: no | proposed
- Proposal path:
""",
    ".agents/templates/proposal.md": """\
# Kit Improvement Proposal: <short-name>

## Problem

-

## Evidence

-

## Proposed Change

-

## Review Gate

- Status: proposed | approved | rejected | implemented
- Reviewer:
- Decision notes:

## Validation Plan

-

## Result

-
""",
    ".agents/templates/retro.md": """\
# Retro: <task-or-date>

## Context

- Task:
- Agent:
- Date:

## What Worked

-

## What Failed Or Was Slow

-

## Reusable Lesson

-

## Promote To Skill?

- Decision: no | proposed | promoted
- Candidate skill name:
- Trigger condition:
""",
    ".agents/templates/skill.md": """\
---
name: skill-name
description: Describe what this skill does and when agents should use it.
disable-model-invocation: true
---

# Skill Name

## When To Use

Use this skill when:

-

## Instructions

1.

## Checks

-

## Anti-Patterns

-
""",
    ".cursor/rules/multi-agent.mdc": """\
---
description: Lightweight multi-agent coordination through .agents/
globs:
alwaysApply: true
---

# Multi-Agent Coordination

Before starting non-trivial work, read `.agents/README.md` and `.agents/STATE.md`
if they exist.

Use `.agents/` only for short-lived coordination:

- `.agents/STATE.md` for shared current context.
- `.agents/agents/*.md` for per-agent session state.
- `.agents/tasks/*.md` for task claims and handoffs.
- `.agents/improve-this-kit/feedback/*.md` for raw usage feedback.
- `.agents/improve-this-kit/proposals/*.md` for review-gated kit improvement proposals.
- `.agents/retros/*.md` for post-task retrospectives.
- `.agents/skills/*/SKILL.md` for reviewed, reusable skills.

Do not overwrite another active agent's state or task file. If work overlaps,
coordinate through a handoff note, branch, or worktree.

Durable decisions belong in `AGENTS.md`, README files, ADRs, or normal project
docs, not transient `.agents/` state.

Feedback, retrospectives, and proposals are evidence. Do not implement proposals
or promote skills without explicit review/approval.
""",
}


@dataclass
class Report:
    created: list[str] = field(default_factory=list)
    existed: list[str] = field(default_factory=list)
    appended: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)


def ensure_file(root: Path, relative_path: str, content: str, report: Report) -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        report.existed.append(relative_path)
        return
    path.write_text(content, encoding="utf-8")
    report.created.append(relative_path)


def has_managed_marker(existing: str) -> bool:
    markers = (NEW_MARKER, *LEGACY_MARKERS)
    return any(f"<!-- {marker}:start -->" in existing for marker in markers)


def append_once(root: Path, relative_path: str, section: str, report: Report) -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        path.write_text(section.rstrip() + "\n", encoding="utf-8")
        report.created.append(relative_path)
        return

    existing = path.read_text(encoding="utf-8")
    if has_managed_marker(existing) or section.rstrip() in existing:
        report.unchanged.append(relative_path)
        return

    separator = "" if existing.endswith("\n") else "\n"
    path.write_text(existing + separator + "\n" + section.rstrip() + "\n", encoding="utf-8")
    report.appended.append(relative_path)


def append_gitignore(root: Path, report: Report) -> None:
    path = root / ".gitignore"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(GITIGNORE_SECTION.rstrip() + "\n", encoding="utf-8")
        report.created.append(".gitignore")
        return

    existing = path.read_text(encoding="utf-8")
    labels = (NEW_MARKER, *LEGACY_MARKERS)
    if any(f"# {label}" in existing for label in labels):
        report.unchanged.append(".gitignore")
        return

    separator = "" if existing.endswith("\n") else "\n"
    path.write_text(existing + separator + "\n" + GITIGNORE_SECTION.rstrip() + "\n", encoding="utf-8")
    report.appended.append(".gitignore")


def create_package(root: Path, package_name: str, report: Report) -> None:
    package_path = package_name.replace("-", "_")
    ensure_file(root, f"src/{package_path}/__init__.py", '"""Project package."""\n', report)


def adapt(target: Path, package_name: str | None = None) -> Report:
    root = target.resolve()
    root.mkdir(parents=True, exist_ok=True)
    report = Report()

    for relative_path, content in FILES.items():
        ensure_file(root, relative_path, content, report)

    append_once(root, "AGENTS.md", AGENTS_SECTION, report)
    append_once(root, "CLAUDE.md", CLAUDE_SECTION, report)
    append_gitignore(root, report)

    if package_name:
        create_package(root, package_name, report)

    return report


def print_report(report: Report) -> None:
    for label, paths in (
        ("created", report.created),
        ("already existed", report.existed),
        ("appended", report.appended),
        ("unchanged", report.unchanged),
    ):
        if paths:
            print(f"{label}:")
            for path in paths:
                print(f"  - {path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="multi-agent-collaboration-kit",
        description="Create or adapt a repository for lightweight multi-agent work.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    adapt_parser = subparsers.add_parser("adapt", help="Add missing agent cooperation files to an existing project.")
    adapt_parser.add_argument("target", type=Path, help="Project directory to adapt.")
    adapt_parser.add_argument("--package-name", help="Optionally create src/<package_name>/__init__.py.")

    new_parser = subparsers.add_parser("new", help="Create a new agent-ready project.")
    new_parser.add_argument("target", type=Path, help="Project directory to create.")
    new_parser.add_argument("--package-name", default="your_package_name", help="Python package name for src layout.")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = adapt(args.target, package_name=args.package_name)
    print_report(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

