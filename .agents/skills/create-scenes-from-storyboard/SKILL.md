---
name: create-scenes-from-storyboard
description: Create scene folders automatically from the storyboard or explicit scene names. Use when the storyboard, shot list, or timing plan is ready and the repo needs `03-scenes/scene-###-*` folders copied from `03-scenes/scene-000-template/`.
---

# Create Scenes From Storyboard

## Purpose

Use this skill when the storyboard is ready and the user wants the scene folders created automatically.

## Input

- `02-storyboard/storyboard.md`
- `02-storyboard/shot-list.md`
- `02-storyboard/timing-plan.md`
- optional `05-final/timeline.yaml`

## Output

Scene folders under:

```txt
03-scenes/
```

Each scene is copied from:

```txt
03-scenes/scene-000-template/
```

## Rule

This is the only scene creation workflow. Do not create scene folders by hand. Use the script below, then fill the scene briefs and prompts.

Each attempt contains:

```txt
attempt_01/
├── 01_first_frame/
├── 02_last_frame/     ← optional; skip if end-frame not needed
└── 03_generated_video/
```

## Command

```bash
uv run python .agents/skills/create-scenes-from-storyboard/scripts/create_scenes_from_storyboard.py
```

The script reads `02-storyboard/shot-list.md` first. If it cannot infer scenes from that file, pass explicit names:

```bash
uv run python .agents/skills/create-scenes-from-storyboard/scripts/create_scenes_from_storyboard.py \
  --scene "Hook - Matcha Pour" \
  --scene "Context - Cafe Counter"
```

To skip last-frame folder and prompt for all scenes:

```bash
uv run python .agents/skills/create-scenes-from-storyboard/scripts/create_scenes_from_storyboard.py --no-last-frame
```

`--no-last-frame` removes `attempt_01/02_last_frame/` and `prompts/last-frame-prompt.md` from every created scene. Use when end-frame control is not needed for this project.
