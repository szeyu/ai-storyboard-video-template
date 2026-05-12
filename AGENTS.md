# AGENTS.md

This repository is an AI storyboard video template.

You are helping the user turn a video idea into:

- a clear brief
- creative ideas
- a selected direction
- storyboard
- scene folders
- generated images/videos/audio
- final combined video
- thumbnails, captions, posting copy, and handoff files

## Main Workflow

Follow this order:

### Phase 1 — Brief

1. Read `00-brief/`
2. Check if the brief is complete enough to proceed
3. If gaps exist, write them in `01-ideas/missing-information.md` and **stop — ask the user to fill the gaps before continuing**
4. Once the brief is complete, proceed

### Phase 2 — Ideas

5. Generate creative ideas and write them in `01-ideas/idea-bank.md`
6. Present ideas to the user and wait for selection
7. Save the chosen direction in `01-ideas/selected-idea.md`

### Phase 3 — Storyboard

8. Create the storyboard in `02-storyboard/storyboard.md`
9. Create shot list in `02-storyboard/shot-list.md`
10. Create timing plan in `02-storyboard/timing-plan.md`

### Phase 4 — Scenes (repeat for each scene)

11. Create scene folder by copying `03-scenes/scene-000-template/`
12. Fill `scene-brief.md` and all prompts in `prompts/`
13. Reference source materials from `04-assets/` where relevant
14. Generate first-frame and last-frame candidates into `first-frame/` and `last-frame/`
15. Use selected first/last frames to generate the scene video
16. Generate images into `generated-images/`
17. Generate videos into `generated-videos/`
18. Generate audio into `generated-audio/`
19. User marks selected files with `_SELECTED` in the filename
20. Repeat steps 11–19 for each remaining scene

### Phase 5 — Assembly

21. Build `05-final/timeline.yaml` using only `_SELECTED` scene videos
22. Optionally render `05-final/storyboard-preview.html` for visual review
23. Assemble final video into `05-final/final-video/`

### Phase 6 — Delivery

24. Create thumbnail candidates in `05-final/thumbnails/`
25. Create captions in `05-final/captions/`
26. Create posting copy in `05-final/posting-copy/`
27. Prepare handoff files in `05-final/client-handoff/`

## Folder Rules

### `00-brief/`

Use this for the user's input:

- project brief
- constraints
- references

### `01-ideas/`

Use this for ideation:

- idea bank
- selected idea
- missing information

If the brief is incomplete, do not block the user. Write missing information clearly and make reasonable assumptions if needed.

### `02-storyboard/`

Use this for the video plan:

- storyboard
- shot list
- timing plan

### `03-scenes/`

Use this for per-scene work.

Each scene should contain:

- scene brief
- image prompt
- video prompt
- audio prompt
- references
- first frame
- last frame
- generated images
- generated videos
- generated audio
- notes

### `04-assets/`

Use this for source materials only.

Examples:

- user-provided images
- user-provided videos
- user-provided audio
- logos
- brand references
- documents

Do not store generated scene outputs here.

### `05-final/`

Use this for final outputs:

- timeline
- final video
- thumbnails
- captions
- posting copy
- client handoff

## Scene Creation Rule

Do not create scene folders from scratch.

Always copy:

```txt
03-scenes/scene-000-template/
```

Then rename the copied folder using this pattern:

```txt
scene-{number}-{short-description}
```

Examples:

```txt
scene-001-hook-matcha-pour
scene-002-context-cafe-counter
scene-003-main-message-product-closeup
scene-004-proof-customer-reaction
scene-005-ending-cta
```

Or use the helper script:

```bash
python skills/create-scene-from-template/scripts/create_scene.py --number 1 --name "hook-matcha-pour"
```

## Scene Folder Rule

Each real scene folder should follow this structure:

```txt
scene-001-example/
├── scene-brief.md
├── prompts/
│   ├── image-prompt.md
│   ├── video-prompt.md
│   └── audio-prompt.md
├── references/
├── first-frame/
├── last-frame/
├── generated-images/
├── generated-videos/
├── generated-audio/
└── notes.md
```

## Asset Naming Rule

Use descriptive filenames.

Pattern:

```txt
{project-slug}_scene{number}_{scene-purpose}_{asset-type}_{style}_v{version}.{ext}
```

Examples:

```txt
matcha-launch_scene001_hook_image_cinematic_v001.png
matcha-launch_scene001_hook_video_cinematic_v001.mp4
matcha-launch_scene001_hook_first-frame_cinematic_v001.png
matcha-launch_scene001_hook_last-frame_cinematic_v001.png
matcha-launch_scene002_context_audio_voiceover_v001.wav
```

When the user selects a file, rename or copy it with `_SELECTED`:

```txt
matcha-launch_scene001_hook_video_SELECTED.mp4
matcha-launch_scene001_hook_first-frame_SELECTED.png
matcha-launch_scene001_hook_last-frame_SELECTED.png
```

## Selection Rule

Do not create `approved/`, `disapproved/`, or `attempts/` folders.

Use filename versioning instead:

```txt
_v001
_v002
_v003
_SELECTED
```

The selected file is the one with `_SELECTED`.

If a file is bad, leave it as versioned history unless the user asks to delete it.

## First Frame and Last Frame Rule

For image-to-video workflows, use:

```txt
first-frame/
last-frame/
```

Store generated first and last frame candidates there.

Examples:

```txt
first-frame/matcha-launch_scene001_first-frame_v001.png
first-frame/matcha-launch_scene001_first-frame_SELECTED.png

last-frame/matcha-launch_scene001_last-frame_v001.png
last-frame/matcha-launch_scene001_last-frame_SELECTED.png
```

Use selected first and last frames to generate the scene video.

## Generated Scene Output Rule

Generated images go here:

```txt
03-scenes/<scene-folder>/generated-images/
```

Generated videos go here:

```txt
03-scenes/<scene-folder>/generated-videos/
```

Generated audio goes here:

```txt
03-scenes/<scene-folder>/generated-audio/
```

Do not place generated scene files in `04-assets/`.

## Final Output Rule

The final combined video goes here:

```txt
05-final/final-video/
```

Thumbnails go here:

```txt
05-final/thumbnails/
```

Captions go here:

```txt
05-final/captions/
```

Posting copy goes here:

```txt
05-final/posting-copy/
```

Client handoff material goes here:

```txt
05-final/client-handoff/
```

## Timeline Rule

Use `05-final/timeline.yaml` to define the final video sequence.

The timeline should reference selected scene videos only.

Example:

```yaml
project:
  name: matcha-launch
  output: matcha-launch_final_v001.mp4
  aspect_ratio: "9:16"
  fps: 30

timeline:
  - scene: scene-001-hook-matcha-pour
    title: "Hook - Matcha Pour"
    purpose: "Stop attention in the first 3 seconds"
    duration: 3
    first_frame: "../03-scenes/scene-001-hook-matcha-pour/first-frame/matcha-launch_scene001_first-frame_SELECTED.png"
    last_frame: "../03-scenes/scene-001-hook-matcha-pour/last-frame/matcha-launch_scene001_last-frame_SELECTED.png"
    video: "../03-scenes/scene-001-hook-matcha-pour/generated-videos/matcha-launch_scene001_hook_video_SELECTED.mp4"
    text_overlay: "New matcha just dropped"
    voiceover: "Something refreshing is here."
    notes: ""

  - scene: scene-002-context-cafe-counter
    title: "Context - Cafe Counter"
    purpose: "Set the scene"
    duration: 5
    first_frame: "../03-scenes/scene-002-context-cafe-counter/first-frame/matcha-launch_scene002_first-frame_SELECTED.png"
    last_frame: "../03-scenes/scene-002-context-cafe-counter/last-frame/matcha-launch_scene002_last-frame_SELECTED.png"
    video: "../03-scenes/scene-002-context-cafe-counter/generated-videos/matcha-launch_scene002_context_video_SELECTED.mp4"
    text_overlay: ""
    voiceover: ""
    notes: ""
```

## Storyboard Preview Rule

Use `skills/render-storyboard-html/` when the user wants to preview the storyboard visually.

The source file is:

```txt
05-final/timeline.yaml
```

The output file is:

```txt
05-final/storyboard-preview.html
```

Run:

```bash
python skills/render-storyboard-html/scripts/render_storyboard_html.py \
  --timeline 05-final/timeline.yaml \
  --output 05-final/storyboard-preview.html
```

The preview should show:

- scene order
- scene title
- purpose
- duration
- first frame
- last frame
- selected video link
- text overlay
- voiceover
- notes

## Tool Rule

This template is tool-neutral.

The first recommended generation tool is Higgsfield, but the structure should work with other tools too.

Possible tools:

- Higgsfield
- Runway
- Kling
- Veo
- Pika
- ComfyUI
- FFmpeg
- Claude Code
- Cursor
- Codex-style agents
- OpenClaw
- Windsurf

If official Higgsfield skills are installed, use them for:

- image generation
- video generation
- style/soul generation
- product photoshoot generation

Do not vendor or duplicate third-party skills into this repo unless the user asks.

Third-party skills may live in hidden folders such as:

```txt
.claude/
.agents/
```

## Repo Skills Rule

Repo-owned workflow skills live in:

```txt
skills/
```

These skills are for local workflow automation, not generation model ownership.

Examples:

- create scene from template
- assemble video with FFmpeg
- add captions
- mix audio
- export platform versions
- quality check video
- prepare social media posting assets

## Social Media Rule

Do not post automatically unless the user explicitly confirms.

The `post-to-social-media` skill should initially prepare posting assets only:

- final video
- caption
- hashtags
- thumbnail
- platform-specific copy

Publishing should require explicit user approval.

## Behavior Rule

Keep the workflow simple for clients.

Prefer clear folders and filenames over complicated tracking documents.

Do not over-engineer the project.
