#!/usr/bin/env python3

import argparse
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
TEMPLATE_DIR = REPO_ROOT / "03-scenes" / "scene-000-template"
SCENES_DIR = REPO_ROOT / "03-scenes"
SHOT_LIST = REPO_ROOT / "02-storyboard" / "shot-list.md"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "scene"


def infer_scene_names() -> list[str]:
    if not SHOT_LIST.exists():
        return []

    names: list[str] = []
    for line in SHOT_LIST.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if not text:
            continue

        heading = re.match(r"^#{2,6}\s+(?:scene\s*\d+\s*[-:]\s*)?(.*)$", text, re.I)
        numbered = re.match(r"^(?:\d+[\).\s-]+|[-*]\s+)(?:scene\s*\d+\s*[-:]\s*)?(.*)$", text, re.I)

        match = heading or numbered
        if not match:
            continue

        name = match.group(1).strip()
        name = re.sub(r"\s+\|\s+.*$", "", name).strip()
        if name and not name.lower().startswith(("shot list", "notes", "timing")):
            names.append(name)

    return names


def create_scene(number: int, name: str, *, no_last_frame: bool = False) -> Path:
    folder_name = f"scene-{number:03d}-{slugify(name)}"
    dest = SCENES_DIR / folder_name

    if dest.exists():
        return dest

    shutil.copytree(TEMPLATE_DIR, dest)

    if no_last_frame:
        last_frame_dir = dest / "attempt_01" / "02_last_frame"
        last_frame_prompt = dest / "prompts" / "last-frame-prompt.md"
        if last_frame_dir.exists():
            shutil.rmtree(last_frame_dir)
        if last_frame_prompt.exists():
            last_frame_prompt.unlink()

    return dest


def main() -> None:
    parser = argparse.ArgumentParser(description="Create scene folders automatically from the storyboard shot list.")
    parser.add_argument("--scene", action="append", default=[], help="Scene name. Can be passed multiple times.")
    parser.add_argument("--no-last-frame", action="store_true", help="Omit last-frame folder and prompt from each scene.")
    args = parser.parse_args()

    if not TEMPLATE_DIR.exists():
        print(f"Error: template not found at {TEMPLATE_DIR}", file=sys.stderr)
        sys.exit(1)

    names = args.scene or infer_scene_names()
    if not names:
        print(
            "Error: no scenes found. Add scenes to 02-storyboard/shot-list.md or pass --scene.",
            file=sys.stderr,
        )
        sys.exit(1)

    for index, name in enumerate(names, start=1):
        dest = create_scene(index, name, no_last_frame=args.no_last_frame)
        print(f"Scene {index:03d}: {dest.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
