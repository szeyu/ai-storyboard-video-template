import argparse
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
TEMPLATE_DIR = REPO_ROOT / "03-scenes" / "scene-000-template"
SCENES_DIR = REPO_ROOT / "03-scenes"


def main():
    parser = argparse.ArgumentParser(description="Create a new scene folder from template.")
    parser.add_argument("--number", type=int, required=True, help="Scene number (e.g. 1)")
    parser.add_argument("--name", type=str, required=True, help="Scene short name (e.g. hook-matcha-pour)")
    args = parser.parse_args()

    scene_folder_name = f"scene-{args.number:03d}-{args.name}"
    dest = SCENES_DIR / scene_folder_name

    if not TEMPLATE_DIR.exists():
        print(f"Error: template not found at {TEMPLATE_DIR}", file=sys.stderr)
        sys.exit(1)

    if dest.exists():
        print(f"Error: folder already exists: {dest}", file=sys.stderr)
        sys.exit(1)

    shutil.copytree(TEMPLATE_DIR, dest)
    print(f"Created: {dest.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
