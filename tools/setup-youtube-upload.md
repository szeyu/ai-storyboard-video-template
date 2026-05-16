# Setup YouTube Upload

Use this guide when configuring local YouTube Data API uploads.

## 1. Install uv

Install `uv` if it is not already available:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Check:

```bash
uv --version
```

## 2. Create the project virtual environment

From the repo root:

```bash
uv venv
uv sync
```

## 3. Create the secrets folder

```bash
mkdir -p .secrets/youtube
```

## 4. Add the OAuth JSON

Move the downloaded Google OAuth Desktop app JSON into:

```txt
.secrets/youtube/client_secrets.json
```

Example:

```bash
mv ~/Downloads/YOUR_LONG_GOOGLE_CLIENT_FILE.json .secrets/youtube/client_secrets.json
```

Do not paste the client ID or client secret into chat, `.env`, README files, workflow files, or scripts.

## 5. Run a private upload

```bash
uv run python .agents/skills/post-to-social-media/scripts/upload_youtube.py \
  --file sandbox.mp4 \
  --title "Sandbox upload test" \
  --description "Private upload test from local storyboard repo." \
  --privacy-status private \
  --made-for-kids false
```

The first run opens a browser for OAuth consent and stores the token at:

```txt
.secrets/youtube/token.json
```

## Common OAuth Failure

If Google shows:

```txt
Access blocked: [app name] has not completed the Google verification process
Error 403: access_denied
```

The OAuth app is probably still in **Testing** mode and the uploading Google account has not been added as a test user.

Fix:

1. Open Google Cloud Console.
2. Select the same project used for `client_secrets.json`.
3. Go to `APIs & Services` -> `OAuth consent screen`.
4. Under `Test users`, add the Google account that will upload the video.
5. Save, then run the upload command again.

You do not need Google app verification for local private testing when the uploader account is listed as a test user.

## Safety

`.gitignore` ignores `.secrets/`, `client_secrets.json`, `token.json`, and `*-oauth2.json`.
