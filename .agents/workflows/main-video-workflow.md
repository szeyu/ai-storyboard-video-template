---
description: Main Video Workflow - Use this workflow to take a project from brief to final delivery.
---

## Phases

1. Brief
   - Read `00-brief/`.
   - If the brief is empty or vague, first follow `.agents/workflows/onboarding-interview-workflow.md`.
   - If generation-blocking gaps exist, write them in `01-ideas/missing-information.md`.
   - Make reasonable assumptions for non-blocking gaps.

2. Ideas
   - Write creative options to `01-ideas/idea-bank.md`.
   - Wait for the chosen direction.
   - Save the chosen direction in `01-ideas/selected-idea.md`.

3. Storyboard
   - Write `02-storyboard/storyboard.md`.
   - Write `02-storyboard/shot-list.md`.
   - Write `02-storyboard/timing-plan.md`.

4. Scenes
   - If product consistency matters, first follow `.agents/workflows/product-reference-workflow.md`.
   - Use `.agents/skills/create-scenes-from-storyboard/`.
   - Then follow `.agents/workflows/scene-attempt-workflow.md`.

5. Assembly
   - Build `05-final/timeline.yaml`.
   - Reference the accepted attempt for each scene.
   - Use `.agents/skills/render-storyboard-html/` for visual review when useful.
   - Use `.agents/skills/assemble-video-ffmpeg/` to create the final video.

6. Delivery
   - Follow `.agents/workflows/delivery-workflow.md`.

## Rules

- Keep source assets in `04-assets/`.
- Keep generated scene outputs inside scene attempt folders.
- `05-final/timeline.yaml` decides the accepted attempt.
- Do not post to social platforms without explicit user approval.
