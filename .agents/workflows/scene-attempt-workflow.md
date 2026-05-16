---
description: Scene Attempt Workflow - Use this workflow for scene generation and scene revisions.
---

## Scene Structure

```txt
scene-001-example/
├── scene-brief.md
├── prompts/
│   ├── first-frame-prompt.md
│   ├── last-frame-prompt.md
│   └── video-prompt.md
└── attempt_01/
    ├── 01_first_frame/
    ├── 02_last_frame/
    └── 03_generated_video/
```

## First Attempt

1. Fill `scene-brief.md`.
2. Fill `prompts/first-frame-prompt.md`.
3. Fill `prompts/last-frame-prompt.md` — **optional**. Skip if a controlled end-frame is not needed or the model does not support it.
4. Fill `prompts/video-prompt.md`.
5. Add useful files from `04-assets/references/` to each prompt's `Source References` section.
6. Generate first-frame candidates into `attempt_01/01_first_frame/`.
7. Generate last-frame candidates into `attempt_01/02_last_frame/` — **optional**. Only do this when a specific end-frame improves the transition or the user requests it.
8. Check whether the selected video model supports audio.
9. Generate video into `attempt_01/03_generated_video/`.
10. Update `05-final/timeline.yaml` to point at the accepted attempt.

## Revision Attempt

When the user asks for a revision:

```bash
uv run python .agents/skills/create-next-attempt/scripts/create_next_attempt.py 03-scenes/scene-001-example
```

Then:

1. Update the prompt files according to the user request.
2. Remove unwanted copied outputs if needed.
3. Regenerate first frame, last frame (optional — skip if not needed), and video in the new attempt.
4. Update `05-final/timeline.yaml` to point to the accepted attempt.

## Audio

- Do not create separate scene audio files by default.
- If the selected video model supports audio, include `Audio Direction` from `prompts/video-prompt.md`.
- If generated video includes usable audio, keep it embedded in the video.
