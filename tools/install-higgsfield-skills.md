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
npx skills add higgsfield-ai/skills1
```

Works with Claude Code, Cursor, Codex, and 12+ other agents.

## Step 4 — Use It

Ask your AI agent:

```txt
Generate an image with Higgsfield using the prompt in:
03-scenes/scene-001-hook-example/prompts/image-prompt.md
```

or:

```txt
Generate a video with Higgsfield using:
- first frame from the scene first-frame folder
- last frame from the scene last-frame folder
- video prompt from the scene prompts folder
```

## Output Rule

Save generated scene files into the matching scene folder:

```txt
03-scenes/<scene-name>/generated-images/
03-scenes/<scene-name>/generated-videos/
03-scenes/<scene-name>/generated-audio/
```

Do not save generated scene files into `04-assets/`.

`04-assets/` is only for source materials provided by the user/client.
