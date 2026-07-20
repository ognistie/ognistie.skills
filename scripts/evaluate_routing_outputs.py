#!/usr/bin/env python3
"""Evaluate captured ognistie.Skill outputs for a selected distribution."""

from __future__ import annotations

import json
import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EVALS_PATH = REPO_ROOT / "evals" / "evals.json"


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top-level JSON value must be an object")
    return data


def parse_outputs(payload: dict) -> list[dict]:
    supplied = payload.get("outputs")
    if not isinstance(supplied, list):
        raise ValueError("outputs must be a list")
    for index, item in enumerate(supplied):
        if (
            not isinstance(item, dict)
            or not isinstance(item.get("id"), int)
            or not isinstance(item.get("output"), str)
        ):
            raise ValueError(f"outputs[{index}] must contain an integer id and string output")
    return supplied


def load_validator(skill_root: Path):
    path = skill_root / "scripts" / "validate_routing_output.py"
    spec = importlib.util.spec_from_file_location("routing_validator", path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load validator from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def evaluate(skill_root: Path, outputs_path: Path) -> list[str]:
    validator = load_validator(skill_root)
    catalog = load_json(skill_root / "references" / "model-catalog.json")
    tiers = {
        (item["name"], item["provider"]): item["tier"]
        for item in catalog["models"]
    }
    cases = {case["id"]: case for case in load_json(EVALS_PATH)["evals"]}
    supplied = parse_outputs(load_json(outputs_path))
    outputs = {item["id"]: item["output"] for item in supplied}
    errors: list[str] = []

    if len(outputs) != len(supplied):
        errors.append("output ids must be unique")

    for case_id, case in cases.items():
        if case_id not in outputs:
            errors.append(f"eval {case_id}: missing output")
            continue

        output = outputs[case_id]
        contract_errors = validator.validate(output)
        errors.extend(f"eval {case_id}: {error}" for error in contract_errors)
        if contract_errors:
            continue

        expected_tier = case["expected_tier"]
        if expected_tier is None:
            if output.strip() != validator.no_task_response():
                errors.append(f"eval {case_id}: expected the no-task response")
            continue

        first_line = output.strip().splitlines()[0]
        match = validator.MODEL_LINE.fullmatch(first_line)
        if match is None:
            continue
        actual_tier = tiers[(match["model"], match["provider"])]
        if actual_tier != expected_tier:
            errors.append(
                f"eval {case_id}: expected tier {expected_tier}, got {actual_tier}"
            )

    unknown_ids = sorted(set(outputs) - set(cases))
    if unknown_ids:
        errors.append(f"unknown eval ids: {unknown_ids}")
    return errors


def main() -> int:
    if len(sys.argv) != 3:
        print(
            "usage: evaluate_routing_outputs.py <skill-dir> <outputs-json>",
            file=sys.stderr,
        )
        return 2
    try:
        errors = evaluate(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
    except (OSError, UnicodeError, ValueError, TypeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("All captured routing outputs match the eval suite.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
