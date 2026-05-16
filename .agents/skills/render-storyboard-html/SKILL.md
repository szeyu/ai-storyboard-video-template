---
name: render-storyboard-html
description: Render `05-final/timeline.yaml` into a local HTML storyboard preview showing scene order, first frames, optional last frames, accepted attempt videos, and notes. Use when the user wants a visual storyboard review.
---

# Render Storyboard HTML

## Purpose

Use this skill when the user wants to preview the storyboard visually in a browser.

This skill converts:

```txt
05-final/timeline.yaml
```

into:

```txt
05-final/storyboard-preview.html
```

## Input

* `05-final/timeline.yaml`
* first frame images referenced in the timeline
* last frame images referenced in the timeline
* accepted attempt videos referenced in the timeline

## Output

* `05-final/storyboard-preview.html`

## Rules

* Use relative paths so the HTML can be opened locally.
* Show first frame and last frame as image previews.
* Show the accepted attempt video as a clickable link.
* Do not embed large video files directly.
* If an image path is missing, show "Missing first frame" or "Missing last frame".
* If a video path is missing, show "Missing video".
* Keep the output simple, clean, and client-friendly.

## Command

```bash
uv run python .agents/skills/render-storyboard-html/scripts/render_storyboard_html.py \
  --timeline 05-final/timeline.yaml \
  --output 05-final/storyboard-preview.html
```
