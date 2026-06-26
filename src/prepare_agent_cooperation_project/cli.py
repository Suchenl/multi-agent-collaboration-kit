from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path


NEW_MARKER = "prepare-agent-cooperation-project"
LEGACY_MARKERS = ("init-agent-native-project",)

AGENTS_SECTION = f"""\
<!-- {NEW_MARKER}:start -->

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
!.agents/agents/.gitkeep
!.agents/tasks/.gitkeep
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
- `templates/agent_state.md`: template for per-agent state.
- `templates/task_state.md`: template for task state.

## Workflow

1. Read `AGENTS.md`, this file, and `STATE.md`.
2. Before editing, note your current task and files you expect to touch.
3. For parallel work, create `.agents/agents/<agent-name>.md` from the template.
4. For claimable tasks, create `.agents/tasks/<task-name>.md` from the template.
5. Keep updates brief and factual.
6. When finished, write a handoff note and mark your state as done.

## Safety Rules

- Do not delete or rewrite another active agent's file.
- Do not claim a file lock forever; include a timestamp and release note.
- If there is a conflict, stop and ask the user or project owner.
- Use git branches or worktrees when work overlaps heavily.
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

Do not overwrite another active agent's state or task file. If work overlaps,
coordinate through a handoff note, branch, or worktree.

Durable decisions belong in `AGENTS.md`, README files, ADRs, or normal project
docs, not transient `.agents/` state.
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
        prog="prepare-agent-cooperation-project",
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

