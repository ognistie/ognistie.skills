#!/usr/bin/env python3
"""Validate the concise ognistie.Skill. routing response."""

from __future__ import annotations

import re
import sys
from pathlib import Path


NO_TASK = "Envie a tarefa que deseja analisar."
MODEL_LINE = re.compile(
    r"^Modelo indicado: (?P<model>[^\r\n]+?) — Provedor: (?P<provider>OpenAI|Anthropic)\.$"
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


def validate(text: str) -> list[str]:
    stripped = text.strip()
    if stripped == NO_TASK:
        return []

    lines = stripped.splitlines()
    errors: list[str] = []
    if len(lines) != 2:
        errors.append("a concrete-task response must contain exactly two non-empty lines")
        return errors

    if not MODEL_LINE.fullmatch(lines[0]):
        errors.append("line 1 must contain the concrete model and OpenAI or Anthropic provider")

    reason_match = REASON_LINE.fullmatch(lines[1])
    if not reason_match:
        errors.append("line 2 must be one complete Motivo sentence ending with a period")
    else:
        reason = reason_match.group("reason")
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
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    errors = validate(text)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Routing output is concise and valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
