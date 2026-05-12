# Create Scene From Template

## Purpose

Use this skill when creating a new scene folder.

## Rule

Always copy:

```txt
03-scenes/scene-000-template/
```

Then rename the copy using:

```txt
scene-{number}-{short-description}
```

## Example

```txt
scene-001-hook-matcha-pour
scene-002-context-cafe-counter
scene-003-main-message-product-closeup
```

## Helper Script

```bash
python skills/create-scene-from-template/scripts/create_scene.py --number 1 --name "hook-matcha-pour"
```

## Output

A new scene folder under:

```txt
03-scenes/
```
