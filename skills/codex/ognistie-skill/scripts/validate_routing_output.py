#!/usr/bin/env python3
"""Validate an ognistie.Skill response for its target runtime."""

from __future__ import annotations

import json
import re
import sys
from functools import lru_cache
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = SKILL_ROOT / "references" / "model-catalog.json"
RUNTIME_PATH = SKILL_ROOT / "references" / "runtime.json"
MODEL_LINE = re.compile(
    r"^Modelo indicado: (?P<model>[^\r\n]+?) — Provedor: "
    r"(?P<provider>OpenAI|Anthropic)\.$"
)
REASON_LINE = re.compile(r"^Motivo: (?P<reason>[^\r\n]+)\.$")


@lru_cache(maxsize=1)
def runtime() -> dict:
    return json.loads(RUNTIME_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def catalog_pairs() -> frozenset[tuple[str, str]]:
    data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    return frozenset((item["name"], item["provider"]) for item in data["models"])


def no_task_response() -> str:
    return (
        "Envie novamente na mesma mensagem: "
        f"{runtime()['invocation']} <sua tarefa>."
    )


def validate(text: str) -> list[str]:
    stripped = text.strip()
    if stripped == no_task_response():
        return []

    lines = stripped.splitlines()
    if len(lines) != 2 or any(not line.strip() for line in lines):
        return ["a concrete-task response must contain exactly two non-empty lines"]

    errors: list[str] = []
    model_match = MODEL_LINE.fullmatch(lines[0])
    if not model_match:
        errors.append("line 1 must contain an exact catalog model and provider")
    elif model_match["provider"] != runtime()["provider"]:
        errors.append("provider does not match the target runtime")
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
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_routing_output.py <output-file>", file=sys.stderr)
        return 2
    try:
        text = Path(sys.argv[1]).read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    errors = validate(text)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Routing output is concise and valid for the target runtime.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
