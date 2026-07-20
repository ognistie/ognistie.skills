#!/usr/bin/env python3
"""Validate the public response contract for ognistie.Skill."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = SKILL_ROOT / "references" / "model-catalog.json"
NO_TASK = "Envie a tarefa que deseja analisar."
MODEL_LINE = re.compile(
    r"^Modelo indicado: (?P<model>[^\r\n]+?) — Provedor: "
    r"(?P<provider>OpenAI|Anthropic)\.$"
)
REASON_LINE = re.compile(r"^Motivo: (?P<reason>[^\r\n]+)\.$")
FORBIDDEN = (
    "Task Analysis",
    "Complexity Level",
    "Recommended Model Tier",
    "Selection Confidence",
    "Delegation Plan",
    "Execution Strategy",
    "Review Required",
    "Next Action",
)


def catalog_pairs() -> set[tuple[str, str]]:
    data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    return {(item["name"], item["provider"]) for item in data["models"]}


def validate(text: str) -> list[str]:
    stripped = text.strip()
    if stripped == NO_TASK:
        return []

    lines = stripped.splitlines()
    errors: list[str] = []
    if len(lines) != 2 or any(not line.strip() for line in lines):
        return ["a concrete-task response must contain exactly two non-empty lines"]

    model_match = MODEL_LINE.fullmatch(lines[0])
    if not model_match:
        errors.append("line 1 must contain the exact model and OpenAI or Anthropic provider")
    elif (model_match["model"], model_match["provider"]) not in catalog_pairs():
        errors.append("model/provider pair is not present in the verified catalog")

    reason_match = REASON_LINE.fullmatch(lines[1])
    if not reason_match:
        errors.append("line 2 must be one Motivo sentence ending with a period")
    else:
        reason = reason_match["reason"].strip()
        if not reason:
            errors.append("the reason must not be empty")
        if len(reason.split()) > 25:
            errors.append("the reason must contain at most 25 words")
        if re.search(r"[.!?](?:\s|$)", reason):
            errors.append("the reason must contain only one sentence")

    for forbidden in FORBIDDEN:
        if forbidden.casefold() in stripped.casefold():
            errors.append(f"forbidden verbose field: {forbidden}")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_routing_output.py <output-file>", file=sys.stderr)
        return 2
    errors = validate(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Routing output is concise and valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
