---
name: assemble-video-ffmpeg
description: Assemble accepted scene attempt videos into a final video with FFmpeg. Use when `05-final/timeline.yaml` references the scene attempt videos that should be combined into `05-final/final-video/`.
---

# Assemble Video with FFmpeg

## Purpose

Use this skill when combining accepted scene attempt videos into one final video.

## Input

- `05-final/timeline.yaml`
- scene videos referenced by `05-final/timeline.yaml`

## Output

- `05-final/final-video/`

## Rule

Only use scene videos referenced by `05-final/timeline.yaml`.

## Command

```bash
uv run python .agents/skills/assemble-video-ffmpeg/scripts/assemble_video.py \
  --timeline 05-final/timeline.yaml
```

The script normalizes every clip before concatenation:

- scales to fit inside the project `resolution`
- pads to the target size
- converts to the project `fps`
- outputs H.264/AAC MP4

Use `--fill crop` when a full-bleed crop is preferred over padding:

```bash
uv run python .agents/skills/assemble-video-ffmpeg/scripts/assemble_video.py \
  --timeline 05-final/timeline.yaml \
  --fill crop
```
