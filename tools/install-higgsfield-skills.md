# Install Higgsfield Skills

This template is tool-neutral, but the first recommended generation tool is Higgsfield.

## Prerequisites

Install Node.js first (required for npm):

```txt
https://nodejs.org
```

Download the LTS version.

## Step 1 — Install the Higgsfield CLI

```bash
npm install -g @higgsfield/cli
```

## Step 2 — Sign In

```bash
higgsfield auth login
```

Opens a browser. Takes 5 seconds. You are now authenticated.

## Step 3 — Add Higgsfield Skills to Your Agent

```bash
npx skills add higgsfield-ai/skills
```

Works with Claude Code, Cursor, Codex, and 12+ other agents.

## Step 4 — Use It

Ask your AI agent:

```txt
Generate an image with Higgsfield using the prompt in:
03-scenes/scene-001-hook-example/prompts/first-frame-prompt.md
```

or:

```txt
Generate a video with Higgsfield using:
- first frame from the scene attempt folder
- optional last frame from the scene attempt folder
- video prompt from the scene prompts folder
```

## Output Rule

Save generated scene files into the matching scene folder:

```txt
03-scenes/<scene-name>/attempt_01/01_first_frame/
03-scenes/<scene-name>/attempt_01/02_last_frame/
03-scenes/<scene-name>/attempt_01/03_generated_video/
```

Do not save generated scene files into `04-assets/`.

`04-assets/` is only for source materials provided by the user/client.

If the selected Higgsfield model supports audio, include audio direction from `prompts/video-prompt.md`. If Higgsfield returns usable audio inside a generated video, keep it with that video.
