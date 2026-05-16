#!/usr/bin/env python3

import argparse
import json
import random
import time
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
]
RETRIABLE_STATUS_CODES = {500, 502, 503, 504}
MAX_RETRIES = 10


def bool_arg(value: str) -> bool:
    lowered = value.lower()
    if lowered in {"true", "1", "yes", "y"}:
        return True
    if lowered in {"false", "0", "no", "n"}:
        return False
    raise argparse.ArgumentTypeError("Expected true or false.")


def load_credentials(client_secrets: Path, token_path: Path) -> Credentials:
    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if not creds or not creds.valid:
        if not client_secrets.exists():
            raise SystemExit(f"Missing OAuth client secrets: {client_secrets}")
        flow = InstalledAppFlow.from_client_secrets_file(str(client_secrets), SCOPES)
        creds = flow.run_local_server(port=0)

    token_path.parent.mkdir(parents=True, exist_ok=True)
    token_path.write_text(creds.to_json(), encoding="utf-8")
    return creds


def upload_video(youtube, args: argparse.Namespace) -> str:
    tags = [tag.strip() for tag in args.keywords.split(",") if tag.strip()]
    body = {
        "snippet": {
            "title": args.title,
            "description": args.description,
            "tags": tags,
            "categoryId": args.category,
        },
        "status": {
            "privacyStatus": args.privacy_status,
            "selfDeclaredMadeForKids": args.made_for_kids,
        },
    }

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=MediaFileUpload(args.file, chunksize=-1, resumable=True),
    )

    response = None
    retry = 0
    while response is None:
        try:
            print("Uploading file...")
            _, response = request.next_chunk()
        except HttpError as exc:
            if exc.resp.status not in RETRIABLE_STATUS_CODES:
                raise
            retry += 1
            if retry > MAX_RETRIES:
                raise SystemExit("Upload failed after retries.") from exc
            sleep_seconds = random.random() * (2**retry)
            print(f"Retriable HTTP {exc.resp.status}; sleeping {sleep_seconds:.1f}s")
            time.sleep(sleep_seconds)

    video_id = response.get("id")
    if not video_id:
        raise SystemExit(f"Unexpected upload response: {json.dumps(response, indent=2)}")
    return video_id


def set_thumbnail(youtube, video_id: str, thumbnail_path: Path) -> None:
    suffix = thumbnail_path.suffix.lower()
    mime = "image/png" if suffix == ".png" else "image/jpeg"
    youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(str(thumbnail_path), mimetype=mime),
    ).execute()
    print(f"Thumbnail set: {thumbnail_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload a video to YouTube with OAuth.")
    parser.add_argument("--file", required=True, help="Video file to upload.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="")
    parser.add_argument("--keywords", default="", help="Comma-separated tags.")
    parser.add_argument("--category", default="22", help="YouTube category ID. Default 22 = People & Blogs.")
    parser.add_argument("--privacy-status", choices=("private", "unlisted", "public"), default="private")
    parser.add_argument("--made-for-kids", type=bool_arg, default=False)
    parser.add_argument("--thumbnail", default=None, help="Thumbnail image path (JPG or PNG). Optional.")
    parser.add_argument("--client-secrets", default=".secrets/youtube/client_secrets.json")
    parser.add_argument("--token", default=".secrets/youtube/token.json")
    args = parser.parse_args()

    video_path = Path(args.file)
    if not video_path.exists():
        raise SystemExit(f"Video file not found: {video_path}")

    thumbnail_path = Path(args.thumbnail) if args.thumbnail else None
    if thumbnail_path and not thumbnail_path.exists():
        raise SystemExit(f"Thumbnail file not found: {thumbnail_path}")

    credentials = load_credentials(Path(args.client_secrets), Path(args.token))
    youtube = build("youtube", "v3", credentials=credentials)
    video_id = upload_video(youtube, args)
    print(f"Uploaded: https://www.youtube.com/watch?v={video_id}")

    if thumbnail_path:
        set_thumbnail(youtube, video_id, thumbnail_path)


if __name__ == "__main__":
    main()
