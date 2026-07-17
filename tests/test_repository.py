from __future__ import annotations

import importlib.util
import re
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "ognistie-skill"
SKILL_MD = SKILL / "SKILL.md"
sys.dont_write_bytecode = True


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load_module("routing_validator", SKILL / "scripts" / "validate_routing_output.py")
packager = load_module("skill_packager", ROOT / "scripts" / "package_skill.py")


class SkillStructureTests(unittest.TestCase):
    def test_frontmatter_name_matches_directory(self):
        text = SKILL_MD.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        self.assertIsNotNone(match)
        frontmatter = match.group(1)
        keys = [line.split(":", 1)[0] for line in frontmatter.splitlines() if ":" in line]
        self.assertEqual(keys, ["name", "description"])
        self.assertIn("name: ognistie-skill", frontmatter)
        self.assertEqual(SKILL.name, "ognistie-skill")

    def test_required_resources_exist(self):
        required = (
            "agents/openai.yaml",
            "references/evals.md",
            "references/examples.md",
            "references/model-tiers.md",
            "scripts/validate_routing_output.py",
        )
        for relative in required:
            self.assertTrue((SKILL / relative).is_file(), relative)

    def test_openai_metadata_names_the_skill(self):
        metadata = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn('display_name: "ognistie.Skill."', metadata)
        self.assertIn("$ognistie-skill", metadata)

    def test_no_machine_specific_paths(self):
        patterns = (r"[A-Za-z]:\\Users\\", r"/Users/[^/<]+/", r"/home/[^/<]+/")
        for path in SKILL.rglob("*"):
            if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
                continue
            text = path.read_text(encoding="utf-8")
            for pattern in patterns:
                self.assertIsNone(re.search(pattern, text), f"{path}: {pattern}")


class RoutingContractTests(unittest.TestCase):
    def test_accepts_concise_response(self):
        output = (
            "Modelo indicado: Claude Sonnet 5 — Provedor: Anthropic.\n"
            "Motivo: Alteração visual moderada oferece boa qualidade com custo menor que modelos avançados."
        )
        self.assertEqual(validator.validate(output), [])

    def test_accepts_no_task_response(self):
        self.assertEqual(validator.validate("Envie a tarefa que deseja analisar."), [])

    def test_rejects_verbose_report(self):
        output = (
            "Task Analysis\n"
            "Modelo indicado: Claude Sonnet 5 — Provedor: Anthropic.\n"
            "Motivo: Boa opção."
        )
        self.assertTrue(validator.validate(output))

    def test_rejects_unknown_provider(self):
        output = (
            "Modelo indicado: Example Model — Provedor: ExampleCorp.\n"
            "Motivo: Boa opção para a tarefa."
        )
        self.assertTrue(validator.validate(output))

    def test_rejects_long_reason(self):
        reason = " ".join(["palavra"] * 26)
        output = (
            "Modelo indicado: GPT-5.6 Terra — Provedor: OpenAI.\n"
            f"Motivo: {reason}."
        )
        self.assertTrue(validator.validate(output))


class PackagingTests(unittest.TestCase):
    def test_archive_contains_portable_top_level_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "ognistie-skill.zip"
            packager.build_archive(output)
            with ZipFile(output) as archive:
                names = archive.namelist()
            self.assertIn("ognistie-skill/SKILL.md", names)
            self.assertTrue(all(name.startswith("ognistie-skill/") for name in names))
            self.assertFalse(any("__pycache__" in name for name in names))


if __name__ == "__main__":
    unittest.main()
