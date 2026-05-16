#!/usr/bin/env python3

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def escape_filter_path(path: Path) -> str:
    text = path.resolve().as_posix()
    return text.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")


def main() -> None:
    parser = argparse.ArgumentParser(description="Burn captions into a video with FFmpeg.")
    parser.add_argument("--input", required=True, help="Input video path.")
    parser.add_argument("--captions", required=True, help="Caption file path (.srt, .vtt, .ass).")
    parser.add_argument("--output", required=True, help="Output video path.")
    parser.add_argument(
        "--style",
        default="FontName=Arial,FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=80",
        help="ASS force_style string for .srt/.vtt subtitles.",
    )
    args = parser.parse_args()

    if shutil.which("ffmpeg") is None:
        print("Error: ffmpeg not found in PATH.", file=sys.stderr)
        sys.exit(1)

    input_path = Path(args.input)
    captions_path = Path(args.captions)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"Error: input video not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    if not captions_path.exists():
        print(f"Error: captions file not found: {captions_path}", file=sys.stderr)
        sys.exit(1)

    if captions_path.suffix.lower() not in {".srt", ".vtt", ".ass"}:
        print("Error: captions must be .srt, .vtt, or .ass.", file=sys.stderr)
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    escaped_captions = escape_filter_path(captions_path)
    if captions_path.suffix.lower() == ".ass":
        video_filter = f"ass='{escaped_captions}'"
    else:
        escaped_style = args.style.replace("'", "\\'")
        video_filter = f"subtitles='{escaped_captions}':force_style='{escaped_style}'"

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
        "copy",
        "-movflags",
        "+faststart",
        str(output_path),
    ]

    subprocess.run(command, check=True)
    print(f"Captioned video written to: {output_path}")


if __name__ == "__main__":
    main()
