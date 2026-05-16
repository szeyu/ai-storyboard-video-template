---
description: Product Reference Workflow - Use this workflow when the product needs consistent multi-angle source-of-truth images before generating scene first frames or last frames.
---

## Goal

Create product reference images that scene prompts can reuse as visual source of truth.

Store these generated reference images in:

```txt
04-assets/references/
```

## When To Use

Use this before scene generation when:

- the product must stay visually consistent across scenes
- packaging, logo, shape, material, or label accuracy matters
- first frames or last frames need reliable product angles
- the user provides source product images in `04-assets/source-images/`

## Reference Angles

Create only the useful angles for the project. Common set:

- front hero
- 3/4 left
- 3/4 right
- side profile
- top detail
- macro label or texture
- product in hand
- product with packaging

## Naming

Use meaningful filenames:

```txt
{project-slug}_product-reference_{angle-or-purpose}_{tool-or-style}_v001.png
```

Examples:

```txt
matcha-launch_product-reference_front-hero_clean-studio_v001.png
matcha-launch_product-reference_3q-left_packaging_v001.png
matcha-launch_product-reference_macro-label_clean-studio_v001.png
```

## Workflow

1. Read `00-brief/` and `04-assets/source-images/`.
2. Identify the product details that must stay consistent.
3. Generate multi-angle product references into `04-assets/references/`.
4. Keep the best versioned files there; do not move them into scene folders.
5. Reference these paths in scene prompt files under `Source References`.
6. Use these references to generate scene first frames and optional last frames.

## Rules

- `04-assets/references/` is for reusable product reference images, not per-scene outputs.
- Per-scene generated frames still belong in `03-scenes/<scene>/attempt_##/`.
- Do not create a reference image if the user-provided source image is already sufficient.
- Do not delete source images from `04-assets/source-images/`.
