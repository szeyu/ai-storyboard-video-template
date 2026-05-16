---
name: add-captions-ffmpeg
description: Add captions or subtitles to final videos with FFmpeg. Use when preparing captioned delivery files from a final video in `05-final/final-video/` and caption files in `05-final/captions/`.
---

# Add Captions with FFmpeg

## Purpose

Use this skill when adding captions or subtitles to the final video.

## Input

- final video from `05-final/final-video/`
- captions from `05-final/captions/`

## Output

- captioned video in `05-final/final-video/`

## Command

Burn captions into the video:

```bash
uv run python .agents/skills/add-captions-ffmpeg/scripts/add_captions.py \
  --input 05-final/final-video/input.mp4 \
  --captions 05-final/captions/captions.srt \
  --output 05-final/final-video/input_captioned.mp4
```

Supported caption formats:

- `.srt`
- `.vtt`
- `.ass`

The script uses FFmpeg and creates hardcoded captions so the result works on platforms that do not preserve subtitle tracks.
