#!/usr/bin/env python3

import argparse
import re
import shutil
import sys
from pathlib import Path

OUTPUT_DIRS = ("01_first_frame", "02_last_frame", "03_generated_video")
ATTEMPT_RE = re.compile(r"^attempt_(\d+)$")


def attempt_number(path: Path) -> int | None:
    match = ATTEMPT_RE.match(path.name)
    if not match:
        return None
    return int(match.group(1))


def find_latest_attempt(scene_dir: Path) -> tuple[int, Path] | None:
    attempts: list[tuple[int, Path]] = []
    for child in scene_dir.iterdir():
        if not child.is_dir():
            continue
        number = attempt_number(child)
        if number is not None:
            attempts.append((number, child))

    if not attempts:
        return None

    return max(attempts, key=lambda item: item[0])


def clear_outputs(attempt_dir: Path) -> None:
    for name in OUTPUT_DIRS:
        output_dir = attempt_dir / name
        output_dir.mkdir(parents=True, exist_ok=True)
        for child in output_dir.iterdir():
            if child.name == ".gitkeep":
                continue
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
        (output_dir / ".gitkeep").touch()


def main() -> None:
    parser = argparse.ArgumentParser(description="Copy the latest scene attempt to the next attempt folder.")
    parser.add_argument("scene_dir", help="Scene folder, e.g. 03-scenes/scene-001-hook")
    parser.add_argument("--keep-outputs", action="store_true", help="Keep copied generated files in the new attempt.")
    args = parser.parse_args()

    scene_dir = Path(args.scene_dir).resolve()
    if not scene_dir.exists() or not scene_dir.is_dir():
        print(f"Error: scene folder not found: {scene_dir}", file=sys.stderr)
        sys.exit(1)

    latest = find_latest_attempt(scene_dir)
    if latest is None:
        print(f"Error: no attempt_## folder found in {scene_dir}", file=sys.stderr)
        sys.exit(1)

    latest_number, latest_path = latest
    next_number = latest_number + 1
    next_path = scene_dir / f"attempt_{next_number:02d}"

    if next_path.exists():
        print(f"Error: next attempt already exists: {next_path}", file=sys.stderr)
        sys.exit(1)

    shutil.copytree(latest_path, next_path)
    if not args.keep_outputs:
        clear_outputs(next_path)

    print(f"Created: {next_path}")


if __name__ == "__main__":
    main()
