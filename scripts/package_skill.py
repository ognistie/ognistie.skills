#!/usr/bin/env python3
"""Build a portable ZIP containing the canonical skill directory."""

from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "ognistie-skill"
SKILL_ROOT = REPOSITORY_ROOT / "skills" / SKILL_NAME


def build_archive(output: Path) -> Path:
    if not (SKILL_ROOT / "SKILL.md").is_file():
        raise FileNotFoundError(f"canonical skill not found: {SKILL_ROOT}")

    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for path in sorted(SKILL_ROOT.rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            relative = path.relative_to(SKILL_ROOT)
            archive.write(path, (Path(SKILL_NAME) / relative).as_posix())

    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=REPOSITORY_ROOT / "dist" / f"{SKILL_NAME}.zip",
        help="archive destination",
    )
    args = parser.parse_args()
    print(build_archive(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
