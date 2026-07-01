import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from mackit.cli import UserCancelled, adapt, main, parse_bundle_selection, resolve_skill_options, selected_bundles_value, toggle_bundle_selection


class IdempotentInstallTest(unittest.TestCase):
    def test_adapt_existing_project_twice_does_not_duplicate_sections(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "AGENTS.md").write_text("# Existing Rules\n", encoding="utf-8")
            (root / "CLAUDE.md").write_text("# Claude Notes\n", encoding="utf-8")
            (root / ".gitignore").write_text(".env\n", encoding="utf-8")

            first = adapt(root)
            second = adapt(root)

            self.assertIn(".agents/README.md", first.created)
            self.assertIn("AGENTS.md", first.appended)
            self.assertIn("AGENTS.md", second.unchanged)

            agents_md = (root / "AGENTS.md").read_text(encoding="utf-8")
            claude_md = (root / "CLAUDE.md").read_text(encoding="utf-8")
            gitignore = (root / ".gitignore").read_text(encoding="utf-8")
            state_md = (root / ".agents" / "STATE.md").read_text(encoding="utf-8")
            rule_md = (root / ".cursor" / "rules" / "multi-agent.mdc").read_text(encoding="utf-8")

            self.assertEqual(agents_md.count("multi-agent-collaboration-kit:start"), 1)
            self.assertEqual(claude_md.count("multi-agent-collaboration-kit:start"), 1)
            self.assertEqual(gitignore.count("# multi-agent-collaboration-kit"), 1)
            self.assertIn("low-frequency shared summary", state_md)
            self.assertIn("source of truth for live work", rule_md)
            self.assertNotIn("update `.agents/STATE.md`", agents_md)

            expected_paths = [
                ".agents/README.md",
                ".agents/STATE.md",
                ".agents/agents/.gitkeep",
                ".agents/retros/.gitkeep",
                ".agents/skills/.gitkeep",
                ".agents/skills/README.md",
                ".agents/skills/external/README.md",
                ".agents/skills/registry.toml",
                ".agents/skills/common/improve-this-kit/SKILL.md",
                ".agents/skills/common/improve-this-kit/reference.md",
                ".agents/skills/common/multi-agent-handoff/SKILL.md",
                ".agents/skills/graphics/xiaobei-skill-image-to-vba/SKILL.md",
                ".agents/skills/graphics/xiaobei-skill-image-to-vba/LICENSE",
                ".agents/skills/graphics/xiaobei-skill-image-to-vba/NOTICE",
                ".agents/skills/graphics/xiaobei-skill-image-to-vba/references/vba-shape-patterns.md",
                ".agents/skills/graphics/xiaobei-skill-image-to-vba/scripts/vba_lint.py",
                ".agents/skills/graphics/paper-framework-figure-studio-pro/SKILL.md",
                ".agents/skills/graphics/paper-framework-figure-studio-pro/metadata.json",
                ".agents/skills/graphics/image-to-editable-ppt/SKILL.md",
                ".agents/skills/graphics/image-to-editable-ppt/cli/pyproject.toml",
                ".agents/skills/graphics/visiomaster/SKILL.md",
                ".agents/skills/graphics/visiomaster/references/scene-schema.md",
                ".agents/skills/research/baseline-selector/SKILL.md",
                ".agents/skills/research/research-paper-writing/SKILL.md",
                ".agents/skills/research/research-paper-writing/references/introduction.md",
                ".agents/skills/research/research-paper-writing/references/method.md",
                ".agents/skills/research/research-paper-writing/references/paper-review.md",
                ".agents/skills/research/research-paper-writing/LICENSE",
                ".agents/skills/review/review-gate/SKILL.md",
                ".agents/skills/workflows/repo-adaptation/SKILL.md",
                ".agents/tasks/.gitkeep",
                ".agents/improve-this-kit/.gitkeep",
                ".agents/improve-this-kit/README.md",
                ".agents/improve-this-kit/feedback/.gitkeep",
                ".agents/improve-this-kit/feedback/README.md",
                ".agents/improve-this-kit/proposals/.gitkeep",
                ".agents/improve-this-kit/proposals/README.md",
                ".agents/templates/agent_state.md",
                ".agents/templates/feedback.md",
                ".agents/templates/proposal.md",
                ".agents/templates/retro.md",
                ".agents/templates/skill.md",
                ".agents/templates/task_state.md",
                ".cursor/rules/multi-agent.mdc",
            ]
            for relative_path in expected_paths:
                self.assertTrue((root / relative_path).exists(), relative_path)

    def test_package_skeleton_is_optional_and_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            first = adapt(root, package_name="demo-package")
            second = adapt(root, package_name="demo-package")

            self.assertIn("src/demo_package/__init__.py", first.created)
            self.assertIn("src/demo_package/__init__.py", second.existed)

    def test_feedback_is_ignored_but_proposals_are_trackable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            adapt(root)

            gitignore = (root / ".gitignore").read_text(encoding="utf-8")
            self.assertIn(".agents/improve-this-kit/feedback/*.md", gitignore)
            self.assertIn("!.agents/improve-this-kit/feedback/README.md", gitignore)
            self.assertIn(".agents/retros/*.md", gitignore)
            self.assertNotIn(".agents/improve-this-kit/proposals/*.md", gitignore)

    def test_can_install_selected_curated_skill_bundles(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            adapt(root, skill_bundles="common,graphics")

            self.assertTrue((root / ".agents/skills/common/multi-agent-handoff/SKILL.md").exists())
            self.assertTrue((root / ".agents/skills/graphics/xiaobei-skill-image-to-vba/SKILL.md").exists())
            self.assertTrue((root / ".agents/skills/graphics/xiaobei-skill-image-to-vba/scripts/vba_lint.py").exists())
            self.assertTrue((root / ".agents/skills/graphics/image-to-editable-ppt/SKILL.md").exists())
            self.assertTrue((root / ".agents/skills/graphics/visiomaster/SKILL.md").exists())
            self.assertFalse((root / ".agents/skills/research/research-paper-writing/SKILL.md").exists())
            self.assertTrue((root / ".agents/skills/common/improve-this-kit/SKILL.md").exists())

    def test_can_skip_curated_skills_but_keep_core_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            adapt(root, install_skills=False)

            self.assertTrue((root / ".agents/skills/common/improve-this-kit/SKILL.md").exists())
            self.assertFalse((root / ".agents/skills/common/multi-agent-handoff/SKILL.md").exists())

    def test_parse_bundle_selection_accepts_numbers_and_names(self) -> None:
        bundles = ["common", "graphics", "research"]

        self.assertEqual(parse_bundle_selection("", bundles), "all")
        self.assertEqual(parse_bundle_selection("all", bundles), "all")
        self.assertEqual(parse_bundle_selection("1,3", bundles), "common,research")
        self.assertEqual(parse_bundle_selection("graphics,1", bundles), "graphics,common")

        with self.assertRaises(ValueError):
            parse_bundle_selection("4", bundles)
        with self.assertRaises(ValueError):
            parse_bundle_selection("unknown", bundles)

    def test_toggle_bundle_selection_supports_checkbox_flow(self) -> None:
        bundles = ["common", "workflows", "graphics"]
        selected = set(bundles)

        selected = toggle_bundle_selection(selected, "workflows", bundles)
        self.assertEqual(selected_bundles_value(selected, bundles), "common,graphics")

        selected = toggle_bundle_selection(selected, "2,graphics", bundles)
        self.assertEqual(selected_bundles_value(selected, bundles), "common,workflows")

        selected = toggle_bundle_selection(selected, "none", bundles)
        self.assertIsNone(selected_bundles_value(selected, bundles))

        selected = toggle_bundle_selection(selected, "all", bundles)
        self.assertEqual(selected_bundles_value(selected, bundles), "all")

    def test_non_interactive_cli_defaults_to_all_skills(self) -> None:
        install_skills, skill_bundles = resolve_skill_options(
            no_curated_skills=False,
            skill_bundles=None,
            yes=False,
            is_interactive=False,
        )

        self.assertTrue(install_skills)
        self.assertEqual(skill_bundles, "all")

    def test_explicit_cli_skill_flags_bypass_interaction(self) -> None:
        self.assertEqual(
            resolve_skill_options(
                no_curated_skills=False,
                skill_bundles="common,graphics",
                yes=False,
                is_interactive=True,
            ),
            (True, "common,graphics"),
        )
        self.assertEqual(
            resolve_skill_options(
                no_curated_skills=True,
                skill_bundles=None,
                yes=False,
                is_interactive=True,
            ),
            (False, None),
        )

    def test_cancelled_interactive_cli_does_not_adapt(self) -> None:
        with (
            patch("mackit.cli.resolve_skill_options", side_effect=UserCancelled),
            patch("mackit.cli.adapt") as adapt_mock,
            patch("sys.stdout", new_callable=StringIO),
        ):
            exit_code = main(["adapt", "."])

        self.assertEqual(exit_code, 130)
        adapt_mock.assert_not_called()

    def test_legacy_markers_prevent_duplicate_managed_sections(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            legacy_section = """\
<!-- init-agent-native-project:start -->

legacy

<!-- init-agent-native-project:end -->
"""
            (root / "AGENTS.md").write_text(legacy_section, encoding="utf-8")
            (root / "CLAUDE.md").write_text(legacy_section, encoding="utf-8")
            (root / ".gitignore").write_text("# init-agent-native-project\n", encoding="utf-8")

            report = adapt(root)

            self.assertIn("AGENTS.md", report.unchanged)
            self.assertIn("CLAUDE.md", report.unchanged)
            self.assertIn(".gitignore", report.unchanged)

            agents_md = (root / "AGENTS.md").read_text(encoding="utf-8")
            claude_md = (root / "CLAUDE.md").read_text(encoding="utf-8")

            self.assertEqual(agents_md.count("multi-agent-collaboration-kit:start"), 0)
            self.assertEqual(claude_md.count("multi-agent-collaboration-kit:start"), 0)
            self.assertEqual(agents_md.count("init-agent-native-project:start"), 1)
            self.assertEqual(claude_md.count("init-agent-native-project:start"), 1)


if __name__ == "__main__":
    unittest.main()

