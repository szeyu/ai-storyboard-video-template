# AGENTS.md

This repository is an AI storyboard video template.

Agents should keep `AGENTS.md` lightweight and read the workflow files in `.agents/workflows/` for operational detail.

## Workflow Routing

- New project onboarding or unclear brief: `.agents/workflows/onboarding-interview-workflow.md`
- Full project from brief to delivery: `.agents/workflows/main-video-workflow.md`
- Scene generation or scene revision: `.agents/workflows/scene-attempt-workflow.md`
- Product multi-angle references: `.agents/workflows/product-reference-workflow.md`
- Final assembly, captions, posting copy, and handoff: `.agents/workflows/delivery-workflow.md`

## Skills

Repo workflow skills live in `.agents/skills/`.

Use these skills through the workflows:

- `.agents/skills/create-scenes-from-storyboard/`
- `.agents/skills/create-next-attempt/`
- `.agents/skills/render-storyboard-html/`
- `.agents/skills/assemble-video-ffmpeg/`
- `.agents/skills/add-captions-ffmpeg/`
- `.agents/skills/post-to-social-media/`

## Folder Rules

- `00-brief/`: user brief, constraints, and references.
- `01-ideas/`: idea bank, missing information, and selected direction.
- `02-storyboard/`: storyboard, shot list, and timing plan.
- `03-scenes/`: scene folders and generation attempts.
- `04-assets/`: source assets and reusable product references only. Do not store generated scene outputs here.
- `05-final/`: timeline, final video, thumbnails, captions, posting copy, and handoff files.
- `.agents/workflows/`: reusable workflow instructions.
- `.agents/skills/`: local automation skills and scripts.

## Core Rules

- Do not create scene folders by hand; use `.agents/skills/create-scenes-from-storyboard/`.
- Ask the user which attempt is acceptable before final assembly.
- Use `05-final/timeline.yaml` as the source of truth for accepted attempts.
- Keep generated scene outputs inside `03-scenes/<scene>/attempt_##/`.
- Keep source images, reusable product references, logos, brand files, and documents in `04-assets/`.
- Do not create separate scene audio files by default. If the selected video model supports audio, include audio direction in the video prompt.
- Do not post to social platforms without explicit user approval.
- For YouTube upload setup, use `tools/setup-youtube-upload.md`.
- Do not ask users to paste OAuth client secrets into chat or `.env`; use `.secrets/`.
- Keep the workflow simple; prefer clear folders and filenames over extra tracking documents.
