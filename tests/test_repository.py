from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from datetime import date, timedelta
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals" / "evals.json"
EVAL_RUNNER = ROOT / "scripts" / "evaluate_routing_outputs.py"
TEXT_SUFFIXES = {".json", ".md", ".py", ".txt", ".yaml", ".yml"}
PLATFORMS = {
    "codex": {
        "root": ROOT / "skills" / "codex" / "ognistie-skill",
        "provider": "OpenAI",
        "invocation": "$ognistie-skill",
    },
    "claude": {
        "root": ROOT / "skills" / "claude" / "ognistie-skill",
        "provider": "Anthropic",
        "invocation": "/ognistie-skill",
    },
}
CLAUDE_MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
CLAUDE_DESKTOP_ZIP = ROOT / "downloads" / "ognistie-skill-claude-desktop.zip"
DEMO_VIDEO = ROOT / "assets" / "ognistie-skill-demo.mp4"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validator(platform: str):
    skill_root = PLATFORMS[platform]["root"]
    return load_module(
        f"routing_validator_{platform}",
        skill_root / "scripts" / "validate_routing_output.py",
    )


class DistributionStructureTests(unittest.TestCase):
    def test_distributions_are_minimal_and_self_contained(self):
        common = {
            "LICENSE.txt",
            "SKILL.md",
            "references/model-catalog.json",
            "references/routing-policy.md",
            "references/runtime.json",
            "scripts/validate_routing_output.py",
        }
        for platform, config in PLATFORMS.items():
            expected = common | (
                {"agents/openai.yaml"}
                if platform == "codex"
                else {".claude-plugin/plugin.json"}
            )
            actual = {
                path.relative_to(config["root"]).as_posix()
                for path in config["root"].rglob("*")
                if path.is_file() and "__pycache__" not in path.parts
            }
            self.assertEqual(actual, expected, platform)

    def test_frontmatter_and_references_are_portable(self):
        for platform, config in PLATFORMS.items():
            text = (config["root"] / "SKILL.md").read_text(encoding="utf-8")
            match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
            self.assertIsNotNone(match, platform)
            keys = [
                line.split(":", 1)[0]
                for line in match.group(1).splitlines()
                if ":" in line
            ]
            self.assertEqual(keys, ["name", "description"], platform)
            self.assertIn("name: ognistie-skill", match.group(1))
            for relative in re.findall(r"\]\((references/[^)]+)\)", text):
                self.assertTrue((config["root"] / relative).is_file(), relative)

    def test_platform_contracts_do_not_leak(self):
        for platform, config in PLATFORMS.items():
            skill = (config["root"] / "SKILL.md").read_text(encoding="utf-8")
            runtime = json.loads(
                (config["root"] / "references" / "runtime.json").read_text()
            )
            self.assertEqual(runtime["provider"], config["provider"])
            self.assertEqual(runtime["invocation"], config["invocation"])
            self.assertIn(config["provider"], skill)
            self.assertIn(config["invocation"], skill)
        claude_skill = (PLATFORMS["claude"]["root"] / "SKILL.md").read_text()
        self.assertIn("$ARGUMENTS", claude_skill)
        self.assertNotIn("/ognistie.skill", claude_skill)

    def test_claude_marketplace_points_to_self_contained_plugin(self):
        marketplace = json.loads(CLAUDE_MARKETPLACE.read_text(encoding="utf-8"))
        self.assertEqual(marketplace["name"], "ognistie-skills")
        self.assertEqual(len(marketplace["plugins"]), 1)
        plugin = marketplace["plugins"][0]
        self.assertEqual(plugin["name"], "ognistie-skill")
        plugin_root = ROOT / plugin["source"]
        self.assertEqual(plugin_root.resolve(), PLATFORMS["claude"]["root"].resolve())
        manifest = json.loads(
            (plugin_root / ".claude-plugin" / "plugin.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(manifest["name"], plugin["name"])
        runtime = json.loads(
            (plugin_root / "references" / "runtime.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            runtime["plugin_invocation"],
            f"/{plugin['name']}:ognistie-skill",
        )

    def test_claude_desktop_download_is_portable_and_documented(self):
        expected = {
            "ognistie-skill/LICENSE.txt",
            "ognistie-skill/SKILL.md",
            "ognistie-skill/references/model-catalog.json",
            "ognistie-skill/references/routing-policy.md",
            "ognistie-skill/scripts/validate_routing_output.py",
        }
        with zipfile.ZipFile(CLAUDE_DESKTOP_ZIP) as archive:
            names = set(archive.namelist())
            self.assertEqual(names, expected)
            self.assertIsNone(archive.testzip())
            self.assertTrue(all("\\" not in name for name in names))
            self.assertTrue(all(".." not in name.split("/") for name in names))

        self.assertGreater(DEMO_VIDEO.stat().st_size, 0)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("assets/ognistie-skill-demo.mp4", readme)
        self.assertIn("downloads/ognistie-skill-claude-desktop.zip", readme)

    def test_shared_files_remain_identical(self):
        codex = PLATFORMS["codex"]["root"]
        claude = PLATFORMS["claude"]["root"]
        for relative in (
            "LICENSE.txt",
            "references/routing-policy.md",
            "scripts/validate_routing_output.py",
        ):
            self.assertEqual(
                (codex / relative).read_bytes(),
                (claude / relative).read_bytes(),
                relative,
            )

    def test_no_machine_paths_or_secrets(self):
        patterns = (
            r"[A-Za-z]:\\Users\\",
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
    def test_catalogs_match_platform_and_are_current(self):
        for platform, config in PLATFORMS.items():
            catalog = json.loads(
                (config["root"] / "references" / "model-catalog.json").read_text()
            )
            models = catalog["models"]
            self.assertTrue(models, platform)
            self.assertEqual({item["provider"] for item in models}, {config["provider"]})
            self.assertEqual({item["tier"] for item in models}, {"economy", "balanced", "advanced"})
            self.assertEqual(len({item["api_id"] for item in models}), len(models))
            self.assertTrue(all(item["input_usd"] > 0 for item in models))
            self.assertTrue(all(item["output_usd"] > 0 for item in models))
            self.assertTrue(
                all(url.startswith("https://") for url in catalog["official_sources"].values())
            )
            expires = date.fromisoformat(catalog["verified_at"]) + timedelta(
                days=catalog["refresh_after_days"]
            )
            self.assertGreaterEqual(expires, date.today())


class EvaluationDatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads(EVALS.read_text(encoding="utf-8"))["evals"]

    def test_dataset_covers_tiers_and_security_boundaries(self):
        self.assertGreaterEqual(len(self.cases), 20)
        self.assertEqual(
            {case["expected_tier"] for case in self.cases},
            {None, "economy", "balanced", "advanced"},
        )
        tags = {tag for case in self.cases for tag in case.get("risk_tags", [])}
        self.assertTrue(
            {
                "prompt-injection",
                "indirect-prompt-injection",
                "provider-boundary",
                "production",
                "authorization",
                "privacy",
            }.issubset(tags)
        )


class RuntimeContractTests(unittest.TestCase):
    def test_each_runtime_accepts_only_its_catalog(self):
        for platform, config in PLATFORMS.items():
            module = validator(platform)
            catalog = json.loads(
                (config["root"] / "references" / "model-catalog.json").read_text()
            )
            for item in catalog["models"]:
                output = (
                    f"Modelo indicado: {item['name']} — Provedor: {item['provider']}.\n"
                    "Motivo: Atende à qualidade necessária com custo proporcional ao risco."
                )
                self.assertEqual(module.validate(output), [], item["name"])
            self.assertEqual(module.validate(module.no_task_response()), [])

    def test_cross_provider_outputs_are_rejected(self):
        codex_validator = validator("codex")
        claude_validator = validator("claude")
        self.assertTrue(
            codex_validator.validate(
                "Modelo indicado: Claude Haiku 4.5 — Provedor: Anthropic.\n"
                "Motivo: Parece barato."
            )
        )
        self.assertTrue(
            claude_validator.validate(
                "Modelo indicado: GPT-5.6 Luna — Provedor: OpenAI.\n"
                "Motivo: Parece barato."
            )
        )

    def test_cli_accepts_utf8_bom(self):
        for platform, config in PLATFORMS.items():
            module = validator(platform)
            model = next(iter(module.catalog_pairs()))
            output = (
                f"Modelo indicado: {model[0]} — Provedor: {model[1]}.\n"
                "Motivo: Bom equilíbrio entre qualidade e custo."
            )
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "output.txt"
                path.write_text(output, encoding="utf-8-sig")
                result = subprocess.run(
                    [
                        sys.executable,
                        str(config["root"] / "scripts" / "validate_routing_output.py"),
                        str(path),
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )
            self.assertEqual(result.returncode, 0, result.stderr)


class CapturedOutputRunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads(EVALS.read_text(encoding="utf-8"))["evals"]

    def outputs_for(self, platform: str) -> list[dict]:
        module = validator(platform)
        catalog = json.loads(
            (PLATFORMS[platform]["root"] / "references" / "model-catalog.json").read_text()
        )["models"]
        by_tier = {item["tier"]: item for item in catalog}
        outputs = []
        for case in self.cases:
            if case["expected_tier"] is None:
                output = module.no_task_response()
            else:
                model = by_tier[case["expected_tier"]]
                output = (
                    f"Modelo indicado: {model['name']} — Provedor: {model['provider']}.\n"
                    "Motivo: Atende à qualidade exigida com custo proporcional ao risco."
                )
            outputs.append({"id": case["id"], "output": output})
        return outputs

    def run_evaluator(self, platform: str, outputs: list[dict]):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "outputs.json"
            path.write_text(json.dumps({"outputs": outputs}), encoding="utf-8")
            return subprocess.run(
                [
                    sys.executable,
                    str(EVAL_RUNNER),
                    str(PLATFORMS[platform]["root"]),
                    str(path),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

    def test_runner_accepts_both_platforms(self):
        for platform in PLATFORMS:
            result = self.run_evaluator(platform, self.outputs_for(platform))
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_runner_rejects_wrong_tier(self):
        outputs = self.outputs_for("codex")
        advanced = next(
            item
            for item in json.loads(
                (PLATFORMS["codex"]["root"] / "references" / "model-catalog.json").read_text()
            )["models"]
            if item["tier"] == "advanced"
        )
        outputs[0]["output"] = (
            f"Modelo indicado: {advanced['name']} — Provedor: OpenAI.\n"
            "Motivo: Modelo mais forte."
        )
        result = self.run_evaluator("codex", outputs)
        self.assertEqual(result.returncode, 1)
        self.assertIn("expected tier economy, got advanced", result.stderr)


if __name__ == "__main__":
    unittest.main()
