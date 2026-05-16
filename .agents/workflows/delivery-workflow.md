---
description: Delivery Workflow - Use this workflow after all scenes are accepted and the final video is ready to assemble and deliver.
---

## Folder Purpose

| Folder | What goes here |
|---|---|
| `05-final/final-video/` | Assembled final video, captioned version |
| `05-final/thumbnails/` | Thumbnail image(s) for the platform |
| `05-final/captions/` | Caption files (`.srt`, `.vtt`, `.ass`) |

---

## Steps

### 1. Confirm timeline

Check `05-final/timeline.yaml` — every scene must reference an accepted attempt and a valid video file path.

### 2. Assemble final video

```bash
uv run python .agents/skills/assemble-video-ffmpeg/scripts/assemble_video.py \
  --timeline 05-final/timeline.yaml
```

Use `--fill crop` for full-bleed crop instead of letterbox padding:

```bash
uv run python .agents/skills/assemble-video-ffmpeg/scripts/assemble_video.py \
  --timeline 05-final/timeline.yaml \
  --fill crop
```

Output lands in `05-final/final-video/`.

### 3. Add captions (optional)

If captions are requested, create or provide a `.srt` / `.vtt` file in `05-final/captions/`, then burn them in:

```bash
uv run python .agents/skills/add-captions-ffmpeg/scripts/add_captions.py \
  --input 05-final/final-video/final.mp4 \
  --captions 05-final/captions/captions.srt \
  --output 05-final/final-video/final_captioned.mp4
```

### 4. Generate thumbnail (optional)

Thumbnails go in `05-final/thumbnails/`. Two options:

**Option A — extract a frame from the final video:**

```bash
ffmpeg -ss <timestamp> -i 05-final/final-video/final.mp4 -frames:v 1 05-final/thumbnails/thumbnail.jpg
```

Replace `<timestamp>` with the timecode of the frame (e.g. `00:00:02`).

**Option B — generate a thumbnail image with AI:**

Use an image generation tool (e.g. Higgsfield image generation). Write a dedicated thumbnail prompt that includes:
- subject and key visual from the video
- platform framing (16:9 for YouTube, 9:16 for Shorts/TikTok)
- text overlay intent (bold title, contrast background) if the user wants text on the thumbnail

Save the generated image to `05-final/thumbnails/thumbnail.jpg` (or `.png`).

Ask the user which option they prefer if not specified.

### 5. Upload to YouTube (only with explicit user approval)

Confirm platform, account, final file, and privacy status before uploading.

```bash
uv run python .agents/skills/post-to-social-media/scripts/upload_youtube.py \
  --file 05-final/final-video/final.mp4 \
  --title "Video title" \
  --description "Description here." \
  --privacy-status private \
  --made-for-kids false \
  --thumbnail 05-final/thumbnails/thumbnail.jpg
```

`--thumbnail` is optional — omit if no thumbnail is prepared.

For YouTube credentials, follow `tools/setup-youtube-upload.md`.

---

## Rules

- Do not publish to any platform without explicit user approval.
- Always confirm the final file path, platform, and account before uploading.
