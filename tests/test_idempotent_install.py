import tempfile
import unittest
from pathlib import Path

from prepare_agent_cooperation_project.cli import adapt


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

            self.assertEqual(agents_md.count("prepare-agent-cooperation-project:start"), 1)
            self.assertEqual(claude_md.count("prepare-agent-cooperation-project:start"), 1)
            self.assertEqual(gitignore.count("# prepare-agent-cooperation-project"), 1)

            expected_paths = [
                ".agents/README.md",
                ".agents/STATE.md",
                ".agents/agents/.gitkeep",
                ".agents/tasks/.gitkeep",
                ".agents/templates/agent_state.md",
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


if __name__ == "__main__":
    unittest.main()

