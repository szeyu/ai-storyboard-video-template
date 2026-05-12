# AI Storyboard Video Template

A reusable template for creating AI-assisted storyboard videos.

This template helps you turn a video idea into:

1. A clear brief
2. Creative ideas
3. A storyboard
4. Scene-by-scene prompts
5. Generated scene images/videos/audio
6. A final assembled video
7. Thumbnails, captions, posting copy, and client handoff files

## Core Workflow

```mermaid
flowchart TD
    START(["`**User**
    Fill 00-brief/`"]) --> READ

    READ["`**AI** reads brief`"] --> CHECK{Brief\ncomplete?}

    CHECK -- gaps found --> MISSING["`Write
    missing-information.md`"]
    MISSING --> FILL(["`**User** fills gaps`"])
    FILL --> READ

    CHECK -- complete --> IDEAS

    IDEAS["`**AI** generates
    idea-bank.md`"] --> SELECT(["`**User** picks idea
    → selected-idea.md`"])

    SELECT --> STORY["`**AI** writes
    storyboard.md
    shot-list.md
    timing-plan.md`"]

    STORY --> COPY["`**AI** copies scene-000-template
    for each scene`"]

    COPY --> SCENE_START

    subgraph SCENE_LOOP["🔁  Repeat for each scene"]
        SCENE_START["`Fill scene-brief.md
        Write prompts/`"]

        ASSETS[("`**04-assets/**
        logos · brand
        source media`")]

        ASSETS -. reference .-> SCENE_START

        SCENE_START --> FRAMES["`Generate first-frame /
        last-frame candidates`"]
        FRAMES --> GEN_IMG["`**Generation tool**
        → generated-images/`"]
        GEN_IMG --> GEN_VID["`**Generation tool**
        → generated-videos/`"]
        GEN_VID --> GEN_AUD["`**Generation tool**
        → generated-audio/`"]
        GEN_AUD --> PICK(["`**User** marks
        filename_SELECTED`"])
    end

    PICK --> MORE{More\nscenes?}
    MORE -- yes --> SCENE_START
    MORE -- no --> TIMELINE

    TIMELINE["`Build
    05-final/timeline.yaml`"] --> PREVIEW["`Optional: render
    storyboard-preview.html`"]

    PREVIEW --> ASSEMBLE["`**AI + FFmpeg**
    Assemble final video
    → 05-final/final-video/`"]

    ASSEMBLE --> DELIVERY

    subgraph DELIVERY["📦  Delivery"]
        THUMB["`thumbnails/`"]
        CAPTIONS["`captions/`"]
        COPY2["`posting-copy/`"]
        HANDOFF["`client-handoff/`"]
    end

    DELIVERY --> DONE(["`✅ Done`"])
```

## Folder Meaning

| Folder           | Purpose                                                                     |
| ---------------- | --------------------------------------------------------------------------- |
| `00-brief/`      | Project brief, constraints, and references                                  |
| `01-ideas/`      | AI-generated ideas, selected idea, and missing information                  |
| `02-storyboard/` | Storyboard, shot list, and timing plan                                      |
| `03-scenes/`     | Scene folders, prompts, first/last frames, generated scene files            |
| `04-assets/`     | Source materials provided by the user/client                                |
| `05-final/`      | Final combined video, thumbnails, captions, posting copy, and handoff files |
| `skills/`        | Local workflow skills for future automation                                 |
| `tools/`         | Setup notes and external tool installation guidance                         |

## Important Rule

`04-assets/` is for source files only.

Generated scene files should go inside the relevant scene folder:

```txt
03-scenes/scene-001-example/generated-images/
03-scenes/scene-001-example/generated-videos/
03-scenes/scene-001-example/generated-audio/
```

Final combined outputs should go into:

```txt
05-final/
```

## Scene Creation

Do not create scene folders manually from scratch.

Copy:

```txt
03-scenes/scene-000-template/
```

Then rename it:

```txt
03-scenes/scene-001-hook-example/
03-scenes/scene-002-context-example/
03-scenes/scene-003-main-message-example/
```

Or use the helper script:

```bash
python skills/create-scene-from-template/scripts/create_scene.py --number 1 --name "hook-matcha-pour"
```

## Selection Rule

Use filename versioning.

Examples:

```txt
scene001_hook_image_v001.png
scene001_hook_image_v002.png
scene001_hook_image_SELECTED.png
```

When a file is selected for final use, include `_SELECTED` in the filename.

The final timeline should use `_SELECTED` files.

## Storyboard HTML Preview

Render `05-final/timeline.yaml` into a browser-friendly storyboard preview:

```bash
python skills/render-storyboard-html/scripts/render_storyboard_html.py \
  --timeline 05-final/timeline.yaml \
  --output 05-final/storyboard-preview.html
```

Then open `05-final/storyboard-preview.html`.

## Start With AI

Open this project in your AI coding tool and ask:

```txt
Read AGENTS.md and help me start a new storyboard video project.
```

## Higgsfield

This template is tool-neutral, but Higgsfield is the first recommended generation tool.

See:

```txt
tools/install-higgsfield-skills.md
```
