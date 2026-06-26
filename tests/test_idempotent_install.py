import tempfile
import unittest
from pathlib import Path

from multi_agent_collaboration_kit.cli import adapt


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

            self.assertEqual(agents_md.count("multi-agent-collaboration-kit:start"), 1)
            self.assertEqual(claude_md.count("multi-agent-collaboration-kit:start"), 1)
            self.assertEqual(gitignore.count("# multi-agent-collaboration-kit"), 1)

            expected_paths = [
                ".agents/README.md",
                ".agents/STATE.md",
                ".agents/agents/.gitkeep",
                ".agents/retros/.gitkeep",
                ".agents/skills/.gitkeep",
                ".agents/skills/README.md",
                ".agents/skills/improve-this-kit/SKILL.md",
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
            self.assertIn(".agents/retros/*.md", gitignore)
            self.assertNotIn(".agents/improve-this-kit/proposals/*.md", gitignore)

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

