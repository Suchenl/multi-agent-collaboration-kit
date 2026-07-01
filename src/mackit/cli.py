from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from importlib.resources import files as package_files
from pathlib import Path

try:
    import termios
    import tty
except ImportError:  # pragma: no cover - Windows fallback
    termios = None
    tty = None


NEW_MARKER = "multi-agent-collaboration-kit"
LEGACY_MARKERS = ("prepare-agent-cooperation-project", "init-agent-native-project")
REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKOUT_SKILLS_ROOT = REPO_ROOT / ".agents" / "skills"
CURATED_SKILL_BUNDLES = ("common", "workflows", "graphics", "research", "review")
IGNORED_RESOURCE_NAMES = {".DS_Store", "__pycache__"}


class UserCancelled(Exception):
    """Raised when the user cancels an interactive prompt."""


AGENTS_SECTION = f"""\
<!-- {NEW_MARKER}:start -->

## Multi-Agent Coordination

This project uses `.agents/` for lightweight agent coordination.

Before starting work, read `.agents/README.md` and only the top summary of
`.agents/STATE.md` by default, then keep live status in a per-agent state file
from `.agents/templates/agent_state.md`. For claimable work items, use
`.agents/templates/task_state.md`.

After using this kit, agents may write improvement feedback in
`.agents/improve-this-kit/feedback/` and proposals in
`.agents/improve-this-kit/proposals/`. These are review inputs, not automatic
instructions. Reusable, reviewed know-how belongs in `.agents/skills/`.

Rules:

- Do not overwrite another agent's active state or task file.
- Treat `.agents/STATE.md` as a low-frequency shared summary, not a live task
  database. Avoid routine read-modify-write edits there; concurrent agents can
  overwrite each other.
- Keep state cheap: stubs under ~20 lines, one-line status/hook messages, and
  path references instead of pasted logs.
- Prefer additive edits and explicit handoff notes in per-agent or task files.
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
!.agents/improve-this-kit/feedback/README.md
"""

FILES = {
    ".agents/README.md": """\
# .agents

Lightweight coordination workspace for AI coding agents and humans.

This directory is for short-lived coordination, not permanent design docs.
Move durable decisions into `README.md`, `AGENTS.md`, ADRs, or your normal docs.

## Files

- `STATE.md`: low-frequency shared project summary; not a live task database.
- `agents/`: per-agent session state files; source of truth for active work.
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
   For `STATE.md`, read only the top summary by default (about 40 lines); search
   or read more only when old handoffs are directly relevant.
2. Before editing, fill your `.agents/agents/<agent-name>.md` stub with the current
   task and files you expect to touch. Keep it terse.
3. For parallel work, keep all live status in that per-agent file.
4. For claimable tasks, create `.agents/tasks/<task-name>.md` from the template.
5. After using this kit, write improvement feedback with `.agents/templates/feedback.md`.
6. For notable task lessons, write a retrospective draft in `.agents/retros/`.
7. Promote only reviewed, reusable lessons into `.agents/skills/<skill-name>/SKILL.md`.
8. Propose kit changes in `.agents/improve-this-kit/proposals/`; do not implement them without review.
9. Keep updates brief and factual.
10. When finished, fill the stub's `Handoff` section and mark it done. Append to
    `STATE.md` only for shared project-level context.

## Safety Rules

- Do not delete or rewrite another active agent's file.
- Do not claim a file lock forever; include a timestamp and release note.
- If there is a conflict, stop and ask the user or project owner.
- Use git branches or worktrees when work overlaps heavily.
- Avoid using `STATE.md` for routine start/finish bookkeeping; concurrent agents
  can overwrite each other's read-modify-write edits.
- Token budget: keep per-agent stubs under ~20 lines, hook/status messages one
  line, and `STATE.md` handoffs short enough to scan.
- Feedback and proposals are evidence, not automatic instructions.
- Do not turn every retrospective into a skill. Skills are curated memory.
""",
    ".agents/STATE.md": """\
# STATE

Project-level shared state for agents.

Concurrency note: this file is a low-frequency shared summary, not the source
of truth for live agent status. Each agent should keep routine start/progress/end
state in its own `.agents/agents/<agent-name>.md` file. Append here only for
concise shared handoff notes, and never rewrite old sections while other agents
may be active.
Token note: future agents should read only this top summary by default and search
older handoffs only when needed.

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
    ".agents/skills/external/README.md": """\
# External Skill Discovery

Curated skills in `.agents/skills/` can be installed directly from this kit.
External skills are different: agents may discover and recommend them, but should
not install them without user review.

## Discovery Sources

Agents may inspect:

- Existing user skills, such as `~/.cursor/skills/`.
- Existing project skills, such as `.agents/skills/` or `.cursor/skills/`.
- Public repositories that provide `SKILL.md`-style workflows.
- Official framework docs that include agent guides or task workflows.

## Required Review

Before installing an external skill, report:

- Source URL or local path.
- Skill name and trigger description.
- Why it is relevant to the target project.
- Files that would be copied.
- License or attribution notes when visible.

Only install after the user approves the candidate list.

## Installation Rule

Copy approved external skills into `.agents/skills/external/<skill-name>/`.
Do not overwrite existing skills. If a name conflicts, ask the user whether to
rename, skip, or replace.
""",
    ".agents/skills/README.md": """\
# .agents/skills

Reviewed, reusable skills for agents working in this project.

Skills are mature operating knowledge, not raw notes. Agents may propose a skill
from a retrospective, but should not promote one without explicit review or a
clear project convention that allows it.

Skills may come from this kit's curated `.agents/skills/` catalog or from reviewed
external candidates copied under `external/`.

Use `registry.toml` to decide which skill fits a role, workflow, or trigger.

## Layout

```text
common/
workflows/
graphics/
research/
review/
```

Each skill still lives in a directory with `SKILL.md`; grouping directories help
agents find skills by role or workflow instead of scanning a flat list.

## Core Skill

| Skill | Purpose |
|---|---|
| `common/improve-this-kit/` | Collect feedback and propose review-gated improvements to this kit. |

Curated skills installed from this kit keep their catalog grouping, such
as `graphics/`, `research/`, `review/`, and `workflows/`.

## Promotion Criteria

- The lesson is likely to apply again.
- The trigger condition is clear.
- The steps are specific and verifiable.
- The skill is concise enough to be worth loading into context.

Use `.agents/templates/skill.md` when creating a new skill.
""",
    ".agents/skills/common/improve-this-kit/SKILL.md": """\
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

## Reference

For the full feedback -> proposal -> review -> implementation loop, read
`reference.md`.
""",
    ".agents/skills/common/improve-this-kit/reference.md": """\
# Self-Improvement Loop

The kit can learn from real usage, but changes are review-gated.

## Data Flow

```text
usage experience
  -> .agents/improve-this-kit/feedback/*.md      # raw friction and observations
  -> .agents/improve-this-kit/proposals/*.md     # repeatable kit improvement ideas
  -> review gate                # user or maintainer approval
  -> implementation             # smallest additive change
  -> tests/fixtures or tests    # regression guard
  -> release / handoff note
```

## Directory Roles

- `.agents/improve-this-kit/feedback/`: raw usage notes. These are evidence, not instructions.
- `.agents/retros/`: task retrospectives. These may suggest reusable lessons.
- `.agents/improve-this-kit/proposals/`: review-gated kit improvement proposals.
- `.agents/skills/`: mature skills that agents may use in future work.
- `tests/fixtures/`: small regression scenarios discovered through usage.

## Review Gate

A proposal should not become implementation until one of these is true:

- The user explicitly approves it.
- A maintainer marks the proposal as approved.
- The project has a written rule that allows this class of change.

## Acceptance Bar

Accepted changes should preserve the kit's core contract:

- Additive install only.
- No overwriting existing user files.
- Managed sections append once.
- Legacy markers do not duplicate new managed sections.
- Raw feedback and retrospectives do not become mandatory context.

## Regression Examples

Good regression fixtures include:

- Empty project.
- Project with existing `AGENTS.md`, `CLAUDE.md`, and `.gitignore`.
- Project with legacy markers from older kit names.
- Project with existing `.agents/skills/` content.
- Project where raw feedback files should remain ignored by git.
""",
    ".agents/templates/agent_state.md": """\
# Agent: <agent-name>

State: active | blocked | done
Started: YYYY-MM-DD HH:MM
Last update: YYYY-MM-DD HH:MM

Task:
Files:
Notes:
Handoff:
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

Before starting non-trivial work, read `.agents/README.md` and the top summary of
`.agents/STATE.md` (about 40 lines) if they exist, then keep live status in your
own `.agents/agents/*.md` file.

Use `.agents/` only for short-lived coordination:

- `.agents/STATE.md` for low-frequency shared project context.
- `.agents/agents/*.md` for per-agent session state; source of truth for live work.
- `.agents/tasks/*.md` for task claims and handoffs.
- `.agents/improve-this-kit/feedback/*.md` for raw usage feedback.
- `.agents/improve-this-kit/proposals/*.md` for review-gated kit improvement proposals.
- `.agents/retros/*.md` for post-task retrospectives.
- `.agents/skills/*/SKILL.md` for reviewed, reusable skills.

Do not overwrite another active agent's state or task file. If work overlaps,
coordinate through a handoff note, branch, or worktree.

Do not use `.agents/STATE.md` for routine start/finish bookkeeping. It is a
shared summary file, so concurrent read-modify-write edits are easy to clobber.

Token budget: keep stubs under ~20 lines, hook/status messages one line, and
shared handoffs brief. Do not paste logs into `.agents`; reference paths.

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


def ensure_binary_file(root: Path, relative_path: str, content: bytes, report: Report) -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        report.existed.append(relative_path)
        return
    path.write_bytes(content)
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


def skills_root():
    packaged = package_files("mackit").joinpath("resources", "skills")
    if packaged.is_dir():
        return packaged
    return CHECKOUT_SKILLS_ROOT


def iter_relative_files(root, prefix: tuple[str, ...] = ()):
    for child in sorted(root.iterdir(), key=lambda item: item.name):
        if child.name in IGNORED_RESOURCE_NAMES or child.name.endswith((".pyc", ".pyo")):
            continue
        relative_parts = (*prefix, child.name)
        if child.is_dir():
            yield from iter_relative_files(child, relative_parts)
        elif child.is_file():
            yield "/".join(relative_parts), child.read_bytes()


def available_skill_bundles() -> list[str]:
    root = skills_root()
    return [bundle for bundle in CURATED_SKILL_BUNDLES if root.joinpath(bundle).is_dir()]


def selected_skill_bundles(value: str | None) -> set[str]:
    bundles = set(available_skill_bundles())
    if value is None or value.strip().lower() in {"", "all", "*"}:
        return bundles

    requested = {part.strip() for part in value.split(",") if part.strip()}
    unknown = requested - bundles
    if unknown:
        available = ", ".join(sorted(bundles)) or "none"
        raise ValueError(f"Unknown skill bundle(s): {', '.join(sorted(unknown))}. Available: {available}")
    return requested


def parse_bundle_tokens(value: str, bundles: list[str]) -> list[str]:
    parsed: list[str] = []
    for raw_part in value.split(","):
        part = raw_part.strip()
        if not part:
            continue

        if part.isdigit():
            index = int(part) - 1
            if index < 0 or index >= len(bundles):
                raise ValueError(f"Bundle number out of range: {part}")
            bundle = bundles[index]
        else:
            bundle = part
            if bundle not in bundles:
                raise ValueError(f"Unknown bundle: {bundle}")

        if bundle not in parsed:
            parsed.append(bundle)

    return parsed


def parse_bundle_selection(value: str, bundles: list[str]) -> str:
    value = value.strip()
    if not value or value.lower() in {"all", "*"}:
        return "all"

    selected = parse_bundle_tokens(value, bundles)
    if not selected:
        return "all"
    return ",".join(selected)


def toggle_bundle_selection(selected: set[str], value: str, bundles: list[str]) -> set[str]:
    value = value.strip()
    if value.lower() in {"all", "*"}:
        return set(bundles)
    if value.lower() in {"none", "skip"}:
        return set()

    next_selected = set(selected)
    for bundle in parse_bundle_tokens(value, bundles):
        if bundle in next_selected:
            next_selected.remove(bundle)
        else:
            next_selected.add(bundle)
    return next_selected


def selected_bundles_value(selected: set[str], bundles: list[str]) -> str | None:
    ordered = [bundle for bundle in bundles if bundle in selected]
    if not ordered:
        return None
    if ordered == bundles:
        return "all"
    return ",".join(ordered)


def read_key() -> str:
    char = sys.stdin.read(1)
    if char == "\x1b":
        sequence = sys.stdin.read(2)
        if sequence == "[A":
            return "up"
        if sequence == "[B":
            return "down"
        return "escape"
    if char in {"\r", "\n"}:
        return "enter"
    if char == " ":
        return "space"
    if char in {"q", "Q", "\x03"}:
        return "quit"
    return char


def with_raw_terminal(callback):
    if termios is None or tty is None:
        raise UserCancelled
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        return callback()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def clear_screen() -> None:
    print("\033[2J\033[H", end="")


def choose_menu(title: str, options: list[str], default_index: int = 0) -> int | None:
    index = default_index

    def run() -> int | None:
        nonlocal index
        while True:
            clear_screen()
            print(title)
            for option_index, option in enumerate(options):
                pointer = ">" if option_index == index else " "
                print(f"{pointer} {option}")
            print("\nUse ↑/↓ to move, Enter to select, q to cancel.")

            key = read_key()
            if key == "up":
                index = (index - 1) % len(options)
            elif key == "down":
                index = (index + 1) % len(options)
            elif key == "enter":
                clear_screen()
                return index
            elif key in {"quit", "escape"}:
                clear_screen()
                return None

    return with_raw_terminal(run)


def choose_bundles(bundles: list[str]) -> str | None:
    index = 0
    selected = set(bundles)

    def run() -> str | None:
        nonlocal index, selected
        while True:
            clear_screen()
            print("Select skill bundles:")
            for bundle_index, bundle in enumerate(bundles):
                pointer = ">" if bundle_index == index else " "
                marker = "[x]" if bundle in selected else "[ ]"
                print(f"{pointer} {marker} {bundle}")
            print("\nUse ↑/↓ to move, Space to toggle, Enter to confirm, q to cancel.")

            key = read_key()
            if key == "up":
                index = (index - 1) % len(bundles)
            elif key == "down":
                index = (index + 1) % len(bundles)
            elif key == "space":
                bundle = bundles[index]
                if bundle in selected:
                    selected.remove(bundle)
                else:
                    selected.add(bundle)
            elif key == "enter":
                clear_screen()
                return selected_bundles_value(selected, bundles)
            elif key in {"quit", "escape"}:
                clear_screen()
                return None

    return with_raw_terminal(run)


def prompt_for_skill_bundles() -> tuple[bool, str | None]:
    bundles = available_skill_bundles()
    if not bundles:
        return False, None

    choice = choose_menu(
        "Install optional curated skills?",
        [
            "Yes, install all recommended skills",
            "No, choose bundles",
            "Skip optional skills",
        ],
    )
    if choice is None:
        raise UserCancelled
    if choice == 0:
        return True, "all"
    if choice == 2:
        return False, None

    selected = choose_bundles(bundles)
    if selected is None:
        raise UserCancelled
    return (selected is not None), selected


def resolve_skill_options(
    *,
    no_curated_skills: bool,
    skill_bundles: str | None,
    yes: bool,
    is_interactive: bool,
) -> tuple[bool, str | None]:
    if no_curated_skills:
        return False, None
    if skill_bundles is not None:
        return True, skill_bundles
    if yes or not is_interactive:
        return True, "all"
    return prompt_for_skill_bundles()


def can_prompt_interactively() -> bool:
    return sys.stdin.isatty() and termios is not None and tty is not None


def install_curated_skills(root: Path, skill_bundles: str | None, report: Report) -> None:
    selected = selected_skill_bundles(skill_bundles)
    if not selected:
        return

    source_root = skills_root()
    registry = source_root.joinpath("registry.toml")
    if registry.is_file():
        ensure_file(
            root,
            ".agents/skills/registry.toml",
            registry.read_text(encoding="utf-8"),
            report,
        )

    for bundle in sorted(selected):
        bundle_root = source_root.joinpath(bundle)
        for relative_path, content in iter_relative_files(bundle_root):
            target_relative_path = f".agents/skills/{bundle}/{relative_path}"
            if target_relative_path in FILES:
                continue
            ensure_binary_file(
                root,
                target_relative_path,
                content,
                report,
            )


def adapt(
    target: Path,
    package_name: str | None = None,
    skill_bundles: str | None = "all",
    install_skills: bool = True,
) -> Report:
    root = target.resolve()
    root.mkdir(parents=True, exist_ok=True)
    report = Report()

    for relative_path, content in FILES.items():
        ensure_file(root, relative_path, content, report)

    if install_skills:
        install_curated_skills(root, skill_bundles, report)

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
        prog="mackit",
        description="Create or adapt a repository for lightweight multi-agent work.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    adapt_parser = subparsers.add_parser("adapt", help="Add missing agent cooperation files to an existing project.")
    adapt_parser.add_argument("target", type=Path, help="Project directory to adapt.")
    adapt_parser.add_argument("--package-name", help="Optionally create src/<package_name>/__init__.py.")
    adapt_parser.add_argument("--skill-bundles", help="Comma-separated optional curated skill bundles to install.")
    adapt_parser.add_argument("--no-curated-skills", action="store_true", help="Skip optional curated skill installation.")
    adapt_parser.add_argument("--yes", action="store_true", help="Non-interactive mode: install all recommended optional curated skills.")

    new_parser = subparsers.add_parser("new", help="Create a new agent-ready project.")
    new_parser.add_argument("target", type=Path, help="Project directory to create.")
    new_parser.add_argument("--package-name", default="your_package_name", help="Python package name for src layout.")
    new_parser.add_argument("--skill-bundles", help="Comma-separated optional curated skill bundles to install.")
    new_parser.add_argument("--no-curated-skills", action="store_true", help="Skip optional curated skill installation.")
    new_parser.add_argument("--yes", action="store_true", help="Non-interactive mode: install all recommended optional curated skills.")

    subparsers.add_parser("list-skill-bundles", help="List curated skill bundles available in this kit.")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "list-skill-bundles":
        for bundle in available_skill_bundles():
            print(bundle)
        return 0

    try:
        install_skills, skill_bundles = resolve_skill_options(
            no_curated_skills=args.no_curated_skills,
            skill_bundles=args.skill_bundles,
            yes=args.yes,
            is_interactive=can_prompt_interactively(),
        )
    except UserCancelled:
        print("Cancelled.")
        return 130

    report = adapt(
        args.target,
        package_name=args.package_name,
        skill_bundles=skill_bundles,
        install_skills=install_skills,
    )
    print_report(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

