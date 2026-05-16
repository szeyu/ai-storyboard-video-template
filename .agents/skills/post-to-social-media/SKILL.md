---
name: post-to-social-media
description: Upload a completed final video to YouTube with optional thumbnail. Never publish without explicit user approval.
---

# Post to Social Media

## Purpose

Use this skill when the final video is ready and the user wants to upload it to YouTube.

## Rules

- Never publish without explicit user approval.
- Always confirm the final file path, title, and privacy status before uploading.
- For YouTube upload credentials, use `tools/setup-youtube-upload.md`.

## YouTube Upload

Use this only after explicit user approval.

```bash
uv run python .agents/skills/post-to-social-media/scripts/upload_youtube.py \
  --file 05-final/final-video/final.mp4 \
  --title "Video title" \
  --description "Description here." \
  --privacy-status private \
  --made-for-kids false \
  --thumbnail 05-final/thumbnails/thumbnail.jpg
```

`--thumbnail` is optional. Omit if no thumbnail is prepared.

The script reads OAuth credentials from `.secrets/youtube/client_secrets.json` and stores tokens in `.secrets/youtube/token.json`.

**Thumbnail requirements:**
- YouTube channel must be phone-verified to set custom thumbnails.
- Thumbnail file must be under 2 MB. JPG or PNG.
- If you previously authenticated without thumbnail support, delete `.secrets/youtube/token.json` and re-run — OAuth will prompt again to grant the expanded scope.
