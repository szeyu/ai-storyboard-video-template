#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:
    raise SystemExit("Missing dependency: PyYAML. Install project dependencies with: uv sync")


def parse_resolution(value: str) -> tuple[int, int]:
    try:
        width_text, height_text = str(value).lower().split("x", 1)
        width = int(width_text)
        height = int(height_text)
    except (ValueError, AttributeError):
        raise SystemExit(f"Invalid resolution: {value!r}. Use WIDTHxHEIGHT, e.g. 1080x1920.")

    if width <= 0 or height <= 0:
        raise SystemExit(f"Invalid resolution: {value!r}. Width and height must be positive.")

    return width, height


def resolve_path(raw_path: str, timeline_path: Path) -> Path:
    path = Path(str(raw_path or "").strip())
    if not path:
        raise SystemExit("Timeline video path is empty.")
    if not path.is_absolute():
        path = timeline_path.parent / path
    return path.resolve()


def escape_concat_path(path: Path) -> str:
    return path.as_posix().replace("'", "'\\''")


def normalize_clip(
    input_path: Path,
    output_path: Path,
    width: int,
    height: int,
    fps: int,
    fill: str,
    background: str,
) -> None:
    if fill == "crop":
        video_filter = (
            f"scale={width}:{height}:force_original_aspect_ratio=increase,"
            f"crop={width}:{height},setsar=1,fps={fps},format=yuv420p"
        )
    else:
        video_filter = (
            f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color={background},"
            f"setsar=1,fps={fps},format=yuv420p"
        )

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-vf",
        video_filter,
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "20",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        str(output_path),
    ]
    subprocess.run(command, check=True)


def concat_clips(clips: list[Path], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        concat_list = Path(f.name)
        for clip in clips:
            f.write(f"file '{escape_concat_path(clip)}'\n")

    try:
        command = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_list),
            "-c",
            "copy",
            "-movflags",
            "+faststart",
            str(output_path),
        ]
        subprocess.run(command, check=True)
    finally:
        concat_list.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize and assemble timeline scene videos with FFmpeg.")
    parser.add_argument("--timeline", default="05-final/timeline.yaml")
    parser.add_argument("--output", help="Override output path.")
    parser.add_argument("--fill", choices=("pad", "crop"), default="pad")
    parser.add_argument("--background", default="black", help="Padding color when --fill pad is used.")
    parser.add_argument("--keep-temp", action="store_true", help="Keep normalized clip files for inspection.")
    args = parser.parse_args()

    if shutil.which("ffmpeg") is None:
        raise SystemExit("Error: ffmpeg not found in PATH.")

    timeline_path = Path(args.timeline).resolve()
    if not timeline_path.exists():
        raise SystemExit(f"Timeline not found: {timeline_path}")

    data = yaml.safe_load(timeline_path.read_text(encoding="utf-8")) or {}
    project = data.get("project", {}) or {}
    timeline = data.get("timeline", []) or []
    if not timeline:
        raise SystemExit("Timeline has no scenes.")

    width, height = parse_resolution(project.get("resolution", "1080x1920"))
    fps = int(project.get("fps", 30))

    output_raw = args.output or project.get("output") or "final-video_v001.mp4"
    output_path = Path(output_raw)
    if not output_path.is_absolute():
        output_path = Path("05-final/final-video") / output_path
    output_path = output_path.resolve()

    temp_dir = Path(tempfile.mkdtemp(prefix="assemble-video-"))
    normalized_clips: list[Path] = []

    try:
        for index, item in enumerate(timeline, start=1):
            video_path = resolve_path(item.get("video", ""), timeline_path)
            if not video_path.exists():
                raise SystemExit(f"Scene {index} video not found: {video_path}")

            normalized = temp_dir / f"{index:03d}_{video_path.stem}.mp4"
            print(f"Normalizing scene {index}: {video_path} -> {normalized}")
            normalize_clip(video_path, normalized, width, height, fps, args.fill, args.background)
            normalized_clips.append(normalized)

        concat_clips(normalized_clips, output_path)
        print(f"Final video written to: {output_path}")
        if args.keep_temp:
            print(f"Normalized clips kept at: {temp_dir}")
            temp_dir = None
    finally:
        if temp_dir is not None:
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
