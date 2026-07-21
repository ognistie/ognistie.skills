#!/usr/bin/env python3
"""Build the portable Claude Desktop skill package."""

from __future__ import annotations

import argparse
import tempfile
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "claude" / "ognistie-skill"
DEFAULT_OUTPUT = REPO_ROOT / "downloads" / "ognistie-skill-claude-desktop.zip"
PACKAGE_ROOT = "ognistie-skill"
TEXT_SUFFIXES = {".json", ".md", ".py", ".txt", ".yaml", ".yml"}
PACKAGE_FILES = (
    "LICENSE.txt",
    "SKILL.md",
    "references/model-catalog.json",
    "references/routing-policy.md",
    "references/runtime.json",
    "scripts/validate_routing_output.py",
)


def canonical_file_bytes(source: Path) -> bytes:
    data = source.read_bytes()
    if source.suffix.lower() not in TEXT_SUFFIXES:
        return data
    text = data.decode("utf-8-sig")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def archive_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    return info


def build_package(destination: Path = DEFAULT_OUTPUT) -> Path:
    destination = destination.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        prefix=f".{destination.stem}-",
        suffix=".tmp",
        dir=destination.parent,
        delete=False,
    ) as temporary_file:
        temporary = Path(temporary_file.name)

    try:
        with zipfile.ZipFile(temporary, "w") as archive:
            for relative in PACKAGE_FILES:
                source = SKILL_ROOT / relative
                if not source.is_file():
                    raise FileNotFoundError(f"package source is missing: {source}")
                archive_name = f"{PACKAGE_ROOT}/{relative}"
                archive.writestr(
                    archive_info(archive_name),
                    canonical_file_bytes(source),
                    compresslevel=9,
                )
        temporary.replace(destination)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise

    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = build_package(args.output)
    print(f"Built {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
