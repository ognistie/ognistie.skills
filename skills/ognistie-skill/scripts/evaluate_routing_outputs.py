#!/usr/bin/env python3
"""Evaluate captured ognistie.Skill outputs against the bundled eval suite."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from validate_routing_output import MODEL_LINE, NO_TASK, validate

SKILL_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = SKILL_ROOT / "references" / "model-catalog.json"
EVALS_PATH = SKILL_ROOT / "evals" / "evals.json"


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


def evaluate(outputs_path: Path) -> list[str]:
    catalog = load_json(CATALOG_PATH)
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
        contract_errors = validate(output)
        errors.extend(f"eval {case_id}: {error}" for error in contract_errors)
        if contract_errors:
            continue

        expected_tier = case["expected_tier"]
        if expected_tier is None:
            if output.strip() != NO_TASK:
                errors.append(f"eval {case_id}: expected the no-task response")
            continue

        first_line = output.strip().splitlines()[0]
        match = MODEL_LINE.fullmatch(first_line)
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
    if len(sys.argv) != 2:
        print("usage: evaluate_routing_outputs.py <outputs-json>", file=sys.stderr)
        return 2
    try:
        errors = evaluate(Path(sys.argv[1]))
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
