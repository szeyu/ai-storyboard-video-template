---
name: create-next-attempt
description: Create the next numbered scene attempt by copying the latest `attempt_##/` folder, clearing generated outputs by default, and preparing the scene for regenerated first frame, optional last frame, and video. Use when revising a scene generation attempt.
---

# Create Next Attempt

## Purpose

Use this skill when a scene needs another generation pass.

The workflow is:

1. Copy the latest `attempt_##/` folder to the next attempt number.
2. Keep prompts and useful reference outputs from the previous attempt.
3. Remove generated images/videos that should be replaced.
4. Regenerate first frame, optional last frame, and video in the new attempt.
5. Ask the user which attempt is acceptable, then update `05-final/timeline.yaml` to point at the accepted attempt and chosen video.

## Command

```bash
uv run python .agents/skills/create-next-attempt/scripts/create_next_attempt.py 03-scenes/scene-001-example
```

By default, generated outputs in the new attempt are cleared after copying.

To keep all copied files:

```bash
uv run python .agents/skills/create-next-attempt/scripts/create_next_attempt.py 03-scenes/scene-001-example --keep-outputs
```

## Attempt Structure

```txt
attempt_01/
├── 01_first_frame/
├── 02_last_frame/     ← optional; skip if end-frame not needed
└── 03_generated_video/
```

## Rule

Use `05-final/timeline.yaml` as the source of truth for accepted attempts.
