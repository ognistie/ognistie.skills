from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "ognistie-skill"
SKILL_MD = SKILL / "SKILL.md"
CATALOG = SKILL / "references" / "model-catalog.json"
EVALS = SKILL / "evals" / "evals.json"
EVAL_RUNNER = SKILL / "scripts" / "evaluate_routing_outputs.py"
TEXT_SUFFIXES = {".json", ".md", ".py", ".txt", ".yaml", ".yml"}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load_module(
    "routing_validator", SKILL / "scripts" / "validate_routing_output.py"
)


class SkillStructureTests(unittest.TestCase):
    def test_frontmatter_is_portable(self):
        text = SKILL_MD.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        self.assertIsNotNone(match)
        frontmatter = match.group(1)
        keys = [
            line.split(":", 1)[0]
            for line in frontmatter.splitlines()
            if ":" in line
        ]
        self.assertEqual(keys, ["name", "description"])
        self.assertIn("name: ognistie-skill", frontmatter)
        self.assertEqual(SKILL.name, "ognistie-skill")

    def test_required_runtime_files_exist(self):
        required = (
            "SKILL.md",
            "LICENSE.txt",
            "agents/openai.yaml",
            "references/routing-policy.md",
            "references/model-catalog.json",
            "evals/evals.json",
            "scripts/evaluate_routing_outputs.py",
            "scripts/validate_routing_output.py",
        )
        for relative in required:
            self.assertTrue((SKILL / relative).is_file(), relative)

    def test_skill_references_existing_files(self):
        text = SKILL_MD.read_text(encoding="utf-8")
        for relative in re.findall(r"\]\((references/[^)]+)\)", text):
            self.assertTrue((SKILL / relative).is_file(), relative)

    def test_no_machine_specific_paths_or_secrets(self):
        patterns = (
            r"[A-Za-z]:\\" + "Users" + r"\\",
            "/" + "Users" + r"/[^/<]+/",
            "/" + "home" + r"/[^/<]+/",
            r"sk-[A-Za-z0-9_-]{20,}",
            r"AKIA[0-9A-Z]{16}",
        )
        for path in ROOT.rglob("*"):
            if (
                not path.is_file()
                or ".git" in path.parts
                or "__pycache__" in path.parts
                or (path.suffix.lower() not in TEXT_SUFFIXES and path.name != "LICENSE")
            ):
                continue
            text = path.read_text(encoding="utf-8-sig")
            for pattern in patterns:
                self.assertIsNone(re.search(pattern, text), f"{path}: {pattern}")


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads(CATALOG.read_text(encoding="utf-8"))

    def test_catalog_has_unique_known_models(self):
        models = self.catalog["models"]
        names = [item["name"] for item in models]
        ids = [item["api_id"] for item in models]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(models), 6)

    def test_catalog_covers_providers_and_tiers(self):
        pairs = {
            (item["provider"], item["tier"])
            for item in self.catalog["models"]
        }
        for provider in ("OpenAI", "Anthropic"):
            for tier in ("economy", "balanced", "advanced"):
                self.assertIn((provider, tier), pairs)

    def test_catalog_uses_official_sources_and_positive_prices(self):
        sources = self.catalog["official_sources"]
        self.assertTrue(sources["OpenAI"].startswith("https://developers.openai.com/"))
        self.assertTrue(
            all(
                url.startswith("https://platform.claude.com/")
                for key, url in sources.items()
                if key.startswith("Anthropic")
            )
        )
        for item in self.catalog["models"]:
            self.assertGreater(item["input_usd"], 0)
            self.assertGreater(item["output_usd"], 0)

    def test_catalog_verification_is_current(self):
        verified_at = date.fromisoformat(self.catalog["verified_at"])
        expires_at = verified_at + timedelta(days=self.catalog["refresh_after_days"])
        self.assertGreaterEqual(expires_at, date.today())


class EvaluationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evals = json.loads(EVALS.read_text(encoding="utf-8"))["evals"]

    def test_eval_suite_is_representative(self):
        self.assertGreaterEqual(len(self.evals), 20)
        tiers = {case["expected_tier"] for case in self.evals}
        self.assertEqual(tiers, {None, "economy", "balanced", "advanced"})

    def test_eval_suite_covers_security_boundaries(self):
        tags = {
            tag
            for case in self.evals
            for tag in case.get("risk_tags", [])
        }
        required = {
            "prompt-injection",
            "indirect-prompt-injection",
            "provider-boundary",
            "production",
            "authorization",
            "privacy",
        }
        self.assertTrue(required.issubset(tags))

    def test_critical_cases_never_expect_lower_tiers(self):
        critical = {
            "production",
            "authorization",
            "credentials",
            "privacy",
            "regulated-data",
            "financial-impact",
        }
        for case in self.evals:
            if critical.intersection(case.get("risk_tags", [])):
                self.assertEqual(case["expected_tier"], "advanced")


class RoutingContractTests(unittest.TestCase):
    def test_accepts_every_catalog_pair(self):
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        for item in catalog["models"]:
            output = (
                f"Modelo indicado: {item['name']} — Provedor: {item['provider']}.\n"
                "Motivo: Este modelo atende à qualidade necessária com custo adequado."
            )
            self.assertEqual(validator.validate(output), [], item["name"])

    def test_accepts_no_task_response(self):
        self.assertEqual(
            validator.validate(
                "Envie novamente na mesma mensagem: $ognistie-skill <sua tarefa>."
            ),
            [],
        )

    def test_rejects_unknown_or_mismatched_model(self):
        outputs = (
            "Modelo indicado: Modelo Inventado — Provedor: OpenAI.\nMotivo: Parece barato.",
            "Modelo indicado: GPT-5.6 Luna — Provedor: Anthropic.\nMotivo: Parece barato.",
        )
        for output in outputs:
            self.assertTrue(validator.validate(output))

    def test_rejects_verbose_or_long_output(self):
        verbose = (
            "Task Analysis\n"
            "Modelo indicado: Claude Sonnet 5 — Provedor: Anthropic.\n"
            "Motivo: Boa opção."
        )
        long_reason = " ".join(["palavra"] * 26)
        long_output = (
            "Modelo indicado: GPT-5.6 Terra — Provedor: OpenAI.\n"
            f"Motivo: {long_reason}."
        )
        self.assertTrue(validator.validate(verbose))
        self.assertTrue(validator.validate(long_output))

    def test_cli_accepts_utf8_bom(self):
        output = (
            "Modelo indicado: GPT-5.6 Terra — Provedor: OpenAI.\n"
            "Motivo: Bom equilíbrio entre qualidade e custo."
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "output.txt"
            path.write_text(output, encoding="utf-8-sig")
            result = subprocess.run(
                [sys.executable, str(SKILL / "scripts" / "validate_routing_output.py"), str(path)],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stderr)


class CapturedOutputEvaluationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads(CATALOG.read_text(encoding="utf-8"))["models"]
        cls.evals = json.loads(EVALS.read_text(encoding="utf-8"))["evals"]

    def run_evaluator(self, outputs: list[dict]) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "outputs.json"
            path.write_text(
                json.dumps({"outputs": outputs}, ensure_ascii=False),
                encoding="utf-8-sig",
            )
            return subprocess.run(
                [sys.executable, str(EVAL_RUNNER), str(path)],
                capture_output=True,
                text=True,
                check=False,
            )

    def output_for_tier(self, tier: str) -> str:
        model = next(item for item in self.catalog if item["tier"] == tier)
        return (
            f"Modelo indicado: {model['name']} — Provedor: {model['provider']}.\n"
            "Motivo: Atende à qualidade exigida com custo proporcional ao risco."
        )

    def build_outputs(self) -> list[dict]:
        outputs = []
        for case in self.evals:
            output = (
                validator.NO_TASK
                if case["expected_tier"] is None
                else self.output_for_tier(case["expected_tier"])
            )
            outputs.append({"id": case["id"], "output": output})
        return outputs

    def test_runner_accepts_outputs_for_all_evals(self):
        outputs = self.build_outputs()
        result = self.run_evaluator(outputs)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_runner_rejects_wrong_tier(self):
        outputs = self.build_outputs()
        outputs[0]["output"] = self.output_for_tier("advanced")
        result = self.run_evaluator(outputs)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("eval 1: expected tier economy, got advanced", result.stderr)

    def test_runner_rejects_invalid_schema_without_traceback(self):
        result = self.run_evaluator([{"id": 1, "output": 42}])
        self.assertEqual(result.returncode, 2)
        self.assertIn("must contain an integer id and string output", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
