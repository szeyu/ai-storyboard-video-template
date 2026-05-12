#!/usr/bin/env python3

import argparse
import html
import os
from pathlib import Path

try:
    import yaml
except ImportError:
    raise SystemExit(
        "Missing dependency: PyYAML\n"
        "Install it with:\n"
        "  pip install pyyaml"
    )


def to_relpath_for_output(raw_path: str, timeline_path: Path, output_path: Path) -> tuple[str, bool]:
    text = str(raw_path or "").strip()
    if not text:
        return "", False

    candidate = Path(text)
    if not candidate.is_absolute():
        candidate = timeline_path.parent / candidate
    candidate = candidate.resolve()

    exists = candidate.exists()

    try:
        rel = os.path.relpath(candidate, output_path.parent)
        return rel.replace("\\", "/"), exists
    except ValueError:
        return candidate.as_posix(), exists


def image_cell(path: str, label: str, exists: bool) -> str:
    if not path or not exists:
        return f'<div class="missing">Missing {html.escape(label)}</div>'

    safe_path = html.escape(path)
    safe_label = html.escape(label)
    return (
        f'<a href="{safe_path}" target="_blank">'
        f'<img src="{safe_path}" alt="{safe_label}" /></a>'
    )


def video_cell(path: str, exists: bool) -> str:
    if not path or not exists:
        return '<div class="missing">Missing video</div>'

    safe_path = html.escape(path)
    return f'<a class="video-link" href="{safe_path}" target="_blank">Open video</a>'


def format_duration(duration: object) -> str:
    if duration is None:
        return ""
    text = str(duration).strip()
    if not text:
        return ""
    if text.endswith("s"):
        return text
    return f"{text}s"


def render_html(data: dict, timeline_path: Path, output_path: Path) -> str:
    project = data.get("project", {}) or {}
    timeline = data.get("timeline", []) or []

    project_name = str(project.get("name", "")).strip() or "Storyboard Preview"
    aspect_ratio = project.get("aspect_ratio", "")
    resolution = project.get("resolution", "")
    fps = project.get("fps", "")

    rows = []

    for index, item in enumerate(timeline, start=1):
        scene = item.get("scene", "")
        title = item.get("title", "")
        purpose = item.get("purpose", "")
        duration = format_duration(item.get("duration", ""))
        text_overlay = item.get("text_overlay", "")
        voiceover = item.get("voiceover", "")
        notes = item.get("notes", "")

        first_frame_path, first_frame_exists = to_relpath_for_output(
            item.get("first_frame", ""), timeline_path, output_path
        )
        last_frame_path, last_frame_exists = to_relpath_for_output(
            item.get("last_frame", ""), timeline_path, output_path
        )
        video_path, video_exists = to_relpath_for_output(
            item.get("video", ""), timeline_path, output_path
        )

        rows.append(
            f"""
            <tr>
              <td class="scene-index">{index}</td>
              <td>
                <div class="scene-name">{html.escape(str(scene))}</div>
                <div class="scene-title">{html.escape(str(title))}</div>
              </td>
              <td>{html.escape(str(purpose))}</td>
              <td>{html.escape(duration)}</td>
              <td>{image_cell(first_frame_path, "first frame", first_frame_exists)}</td>
              <td>{image_cell(last_frame_path, "last frame", last_frame_exists)}</td>
              <td>{video_cell(video_path, video_exists)}</td>
              <td>{html.escape(str(text_overlay))}</td>
              <td>{html.escape(str(voiceover))}</td>
              <td>{html.escape(str(notes))}</td>
            </tr>
            """
        )

    rows_html = (
        "\n".join(rows)
        if rows
        else """
    <tr>
      <td colspan="10" class="empty">No timeline scenes found.</td>
    </tr>
    """
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>{html.escape(project_name)} - Storyboard Preview</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    body {{
      margin: 0;
      padding: 32px;
      font-family: Arial, Helvetica, sans-serif;
      background: #f7f7f8;
      color: #1f2937;
    }}

    header {{
      margin-bottom: 24px;
    }}

    h1 {{
      margin: 0 0 8px;
      font-size: 28px;
    }}

    .meta {{
      color: #6b7280;
      font-size: 14px;
    }}

    .table-wrap {{
      overflow-x: auto;
      background: white;
      border: 1px solid #e5e7eb;
      border-radius: 12px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 1200px;
    }}

    th, td {{
      padding: 14px;
      border-bottom: 1px solid #e5e7eb;
      vertical-align: top;
      font-size: 14px;
    }}

    th {{
      background: #f3f4f6;
      text-align: left;
      font-weight: 700;
      color: #374151;
      position: sticky;
      top: 0;
      z-index: 1;
    }}

    tr:last-child td {{
      border-bottom: none;
    }}

    img {{
      width: 140px;
      max-height: 220px;
      object-fit: cover;
      border-radius: 8px;
      border: 1px solid #e5e7eb;
      background: #f9fafb;
    }}

    .scene-index {{
      font-weight: 700;
      color: #111827;
      width: 48px;
    }}

    .scene-name {{
      font-weight: 700;
      margin-bottom: 4px;
      color: #111827;
    }}

    .scene-title {{
      color: #6b7280;
    }}

    .video-link {{
      display: inline-block;
      padding: 8px 10px;
      border-radius: 8px;
      background: #111827;
      color: white;
      text-decoration: none;
      font-size: 13px;
    }}

    .video-link:hover {{
      background: #374151;
    }}

    .missing {{
      color: #b45309;
      background: #fffbeb;
      border: 1px solid #fde68a;
      border-radius: 8px;
      padding: 8px;
      font-size: 13px;
    }}

    .empty {{
      text-align: center;
      color: #6b7280;
      padding: 32px;
    }}

    footer {{
      margin-top: 20px;
      color: #6b7280;
      font-size: 12px;
    }}
  </style>
</head>
<body>
  <header>
    <h1>{html.escape(project_name)} - Storyboard Preview</h1>
    <div class="meta">
      Aspect Ratio: {html.escape(str(aspect_ratio))} |
      Resolution: {html.escape(str(resolution))} |
      FPS: {html.escape(str(fps))}
    </div>
  </header>

  <main class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>Scene</th>
          <th>Purpose</th>
          <th>Duration</th>
          <th>First Frame</th>
          <th>Last Frame</th>
          <th>Video</th>
          <th>Text Overlay</th>
          <th>Voiceover</th>
          <th>Notes</th>
        </tr>
      </thead>
      <tbody>
        {rows_html}
      </tbody>
    </table>
  </main>

  <footer>Generated from timeline.yaml.</footer>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeline", default="05-final/timeline.yaml")
    parser.add_argument("--output")
    args = parser.parse_args()

    timeline_path = Path(args.timeline).resolve()

    if not timeline_path.exists():
        raise FileNotFoundError(f"Timeline file not found: {timeline_path}")

    with timeline_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    project = data.get("project", {}) or {}
    output_raw = args.output or project.get("storyboard_preview", "05-final/storyboard-preview.html")
    output_path = Path(output_raw).resolve()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    html_content = render_html(data, timeline_path, output_path)
    with output_path.open("w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Storyboard preview written to: {output_path}")


if __name__ == "__main__":
    main()
