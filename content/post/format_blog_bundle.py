#!/usr/bin/env python3
"""Format a Hugo leaf bundle post from an index draft and sibling files."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


POSTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = POSTS_DIR.parent.parent
TZ = dt.timezone(dt.timedelta(hours=8))

IMAGE_EXTS = {".avif", ".gif", ".jpeg", ".jpg", ".png", ".svg", ".webp"}
TEXT_EXTS = {".csv", ".log", ".txt"}
INDEX_RE = re.compile(r"^index(?:\.[A-Za-z-]+)?\.md$")
FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.S)
OBSIDIAN_EMBED_RE = re.compile(r"!\[\[([^\]]+)\]\]")
DEEPSEEK_MODEL = "deepseek-v4-flash"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Hugo front matter and attachment sections for a post bundle."
    )
    parser.add_argument(
        "bundle",
        nargs="?",
        default="26-06-11随笔",
        help="Post bundle directory, relative to content/post unless absolute.",
    )
    return parser.parse_args()


def resolve_bundle(bundle: str) -> Path:
    path = Path(bundle).expanduser()
    if not path.is_absolute():
        path = POSTS_DIR / path
    return path.resolve()


def strip_front_matter(text: str) -> tuple[dict[str, object], str]:
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}, text

    metadata = parse_simple_yaml(match.group(1))
    return metadata, text[match.end() :]


def parse_simple_yaml(raw: str) -> dict[str, object]:
    metadata: dict[str, object] = {}
    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            i += 1
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value:
            metadata[key] = value.strip("\"'")
            i += 1
            continue

        items: list[str] = []
        j = i + 1
        while j < len(lines):
            item_line = lines[j]
            if re.match(r"^\s+-\s+", item_line):
                items.append(re.sub(r"^\s+-\s+", "", item_line).strip().strip("\"'"))
                j += 1
                continue
            if item_line.strip() == "":
                j += 1
                continue
            break
        metadata[key] = items
        i = j
    return metadata


def clean_markdown_body(body: str) -> str:
    body = body.replace("\r\n", "\n").replace("\r", "\n")
    body = remove_generated_attachment_section(body)
    cleaned_lines: list[str] = []
    for line in body.splitlines():
        if OBSIDIAN_EMBED_RE.fullmatch(line.strip()):
            continue
        cleaned_lines.append(convert_obsidian_embeds(line.rstrip()))

    text = "\n".join(cleaned_lines).strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def remove_generated_attachment_section(body: str) -> str:
    marker = "\n## 附件\n"
    if marker in body:
        return body.split(marker, 1)[0].rstrip()
    if body.startswith("## 附件\n"):
        return ""
    return body


def convert_obsidian_embeds(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        target = match.group(1).split("|", 1)[0].strip()
        stem = Path(target).stem
        suffix = Path(target).suffix.lower()
        if suffix in IMAGE_EXTS:
            return f"![{stem}](<{target}>)"
        return f"[{stem}](<{target}>)"

    return OBSIDIAN_EMBED_RE.sub(replace, text)


def list_bundle_files(bundle_dir: Path) -> list[Path]:
    files = [
        path
        for path in bundle_dir.iterdir()
        if path.is_file() and not INDEX_RE.match(path.name) and not path.name.startswith(".")
    ]

    def sort_key(path: Path) -> tuple[int, str]:
        suffix = path.suffix.lower()
        if suffix == ".md":
            priority = 0
        elif suffix == ".pdf":
            priority = 1
        elif suffix in IMAGE_EXTS:
            priority = 2
        elif suffix in TEXT_EXTS:
            priority = 3
        else:
            priority = 4
        return priority, path.name.casefold()

    return sorted(files, key=sort_key)


def file_title(path: Path) -> str:
    if path.suffix.lower() == ".md":
        text = path.read_text(encoding="utf-8")
        _, body = strip_front_matter(text)
        for line in body.splitlines():
            match = re.match(r"^\s*#\s+(.+?)\s*$", line)
            if match:
                return match.group(1)
    return path.stem


def markdown_link(label: str, relative_path: str) -> str:
    return f"[{label}](<{relative_path}>)"


def pdf_text(path: Path) -> str:
    if not shutil.which("pdftotext"):
        return ""
    result = subprocess.run(
        ["pdftotext", str(path), "-"],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0:
        return ""
    return re.sub(r"\n{3,}", "\n\n", result.stdout.replace("\f", "").strip())


def render_attachment(path: Path, bundle_dir: Path) -> str:
    rel = path.relative_to(bundle_dir).as_posix()
    if path.suffix.lower() in IMAGE_EXTS:
        return f"![{file_title(path)}](<{rel}>)"
    if path.suffix.lower() == ".md":
        page_dir = markdown_attachment_page_dir(bundle_dir, path)
        return f"- {markdown_link(file_title(path), page_url(page_dir))}"
    return f"- {markdown_link(path.name, rel)}"


def render_attachments(files: list[Path], bundle_dir: Path) -> str:
    if not files:
        return ""
    rendered = [render_attachment(path, bundle_dir) for path in files]
    return "## 附件\n\n" + "\n".join(rendered)


def markdown_attachment_page_dir(bundle_dir: Path, source_path: Path) -> Path:
    return POSTS_DIR / f"{bundle_dir.name}-{source_path.stem}"


def page_url(page_dir: Path) -> str:
    return f"/post/{urllib.parse.quote(page_dir.name)}/"


def remove_leading_h1(body: str, title: str) -> str:
    lines = body.splitlines()
    if lines and re.fullmatch(rf"\s*#\s+{re.escape(title)}\s*", lines[0]):
        return "\n".join(lines[1:]).lstrip()
    return body


def render_attachment_page_front_matter(
    title: str,
    parent_title: str,
    date_value: str,
    lastmod_value: str,
) -> str:
    lines = [
        "---",
        f"title: {yaml_scalar(title)}",
        f"description: {yaml_scalar(parent_title + ' 的附件页面')}",
        "",
        f"date: {date_value}",
        f"lastmod: {lastmod_value}",
        "",
        "build:",
        "  list: never",
        "  render: always",
        "---",
        "",
    ]
    return "\n".join(lines) + "\n"


def write_markdown_attachment_pages(
    files: list[Path],
    bundle_dir: Path,
    parent_title: str,
    date_value: str,
    lastmod_value: str,
    lastmod_time: dt.datetime,
) -> list[Path]:
    written: list[Path] = []
    for path in files:
        if path.suffix.lower() != ".md":
            continue
        title = file_title(path)
        raw = path.read_text(encoding="utf-8")
        _, body = strip_front_matter(raw)
        body = remove_leading_h1(clean_markdown_body(body), title)
        page_dir = markdown_attachment_page_dir(bundle_dir, path)
        page_dir.mkdir(parents=True, exist_ok=True)
        page_path = page_dir / "index.md"
        output = (
            render_attachment_page_front_matter(title, parent_title, date_value, lastmod_value)
            + body.rstrip()
            + "\n"
        )
        page_path.write_text(output, encoding="utf-8")
        os.utime(page_path, (lastmod_time.timestamp(), lastmod_time.timestamp()))
        written.append(page_path)
    return written


def infer_datetime(index_path: Path, metadata: dict[str, object]) -> tuple[str, str, dt.datetime]:
    existing_date = as_text(metadata.get("date"))
    existing_lastmod = as_text(metadata.get("lastmod"))
    index_mtime = dt.datetime.fromtimestamp(index_path.stat().st_mtime, TZ)
    index_mtime_value = format_datetime(index_mtime)

    if existing_date or existing_lastmod:
        date_value = existing_date or index_mtime_value
        lastmod_value = index_mtime_value
        return date_value, lastmod_value, index_mtime

    return index_mtime_value, index_mtime_value, index_mtime


def format_datetime(value: dt.datetime) -> str:
    return value.astimezone(TZ).replace(microsecond=0).isoformat()


def as_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def content_excerpt(index_body: str, files: list[Path]) -> str:
    chunks = [index_body]
    for path in files:
        suffix = path.suffix.lower()
        if suffix == ".md":
            text = path.read_text(encoding="utf-8")
            _, body = strip_front_matter(text)
            chunks.append(body)
        elif suffix == ".pdf":
            extracted = pdf_text(path)
            if extracted:
                chunks.append(extracted)
        elif suffix in TEXT_EXTS:
            chunks.append(path.read_text(encoding="utf-8", errors="replace"))
    text = "\n\n".join(chunks)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:5000]


def ai_metadata(title: str, excerpt: str, existing_tags: list[str]) -> dict[str, object]:
    api_key = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("DPSK_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY or DPSK_API_KEY is required")

    base_url = (
        os.environ.get("DEEPSEEK_BASE_URL")
        or os.environ.get("DPSK_BASE_URL")
        or "https://api.deepseek.com"
    ).rstrip("/")
    endpoint = f"{base_url}/chat/completions"

    prompt = {
        "title": title,
        "content_excerpt": excerpt,
        "existing_tags_in_blog": existing_tags,
        "rules": [
            "Return strict JSON only.",
            "description must be a concise Chinese summary under 36 Chinese characters.",
            "categories should contain 1 item, prefer existing categories such as 随笔 or 日记.",
            "tags should contain 2 to 5 concise Chinese tags.",
            "For personal short-form writing, include 随想 when suitable.",
        ],
        "schema": {
            "description": "string",
            "categories": ["string"],
            "tags": ["string"],
        },
    }
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You choose Hugo blog metadata for a Chinese personal blog.",
            },
            {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            body = json.loads(response.read().decode("utf-8"))
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"DeepSeek metadata request failed: {exc}") from exc

    content = (
        body.get("choices", [{}])[0]
        .get("message", {})
        .get("content", "")
        .strip()
    )
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, re.S)
        if not match:
            raise RuntimeError("DeepSeek metadata response was not valid JSON")
        try:
            parsed = json.loads(match.group(0))
        except json.JSONDecodeError as exc:
            raise RuntimeError("DeepSeek metadata response was not valid JSON") from exc

    description = as_text(parsed.get("description"))
    categories = normalize_list(parsed.get("categories"))
    tags = normalize_list(parsed.get("tags"))
    if not description or not categories or not tags:
        raise RuntimeError("DeepSeek metadata response missed required fields")
    return {"description": description, "categories": categories[:2], "tags": unique(tags)[:5]}


def normalize_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [as_text(item) for item in value if as_text(item)]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def collect_existing_tags() -> list[str]:
    tags: list[str] = []
    for index in sorted(POSTS_DIR.glob("*/index.md")):
        try:
            text = index.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        metadata, _ = strip_front_matter(text)
        tags.extend(normalize_list(metadata.get("tags")))
    return unique(tags)


def yaml_scalar(value: str) -> str:
    if not value:
        return '""'
    if re.search(r"[:#\[\]{}]|^\s|\s$", value):
        return json.dumps(value, ensure_ascii=False)
    return value


def render_front_matter(
    title: str,
    description: str,
    date_value: str,
    lastmod_value: str,
    categories: list[str],
    tags: list[str],
) -> str:
    lines = [
        "---",
        f"title: {yaml_scalar(title)}",
        f"description: {yaml_scalar(description)}",
        "",
        f"date: {date_value}",
        f"lastmod: {lastmod_value}",
        "",
        "categories:",
    ]
    lines.extend(f"  - {yaml_scalar(item)}" for item in categories)
    lines.append("tags:")
    lines.extend(f"  - {yaml_scalar(item)}" for item in tags)
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def main() -> int:
    args = parse_args()
    bundle_dir = resolve_bundle(args.bundle)
    index_path = bundle_dir / "index.md"
    if not bundle_dir.is_dir():
        print(f"Bundle directory not found: {bundle_dir}", file=sys.stderr)
        return 1
    if not index_path.is_file():
        print(f"index.md not found: {index_path}", file=sys.stderr)
        return 1

    raw = index_path.read_text(encoding="utf-8")
    original_metadata, raw_body = strip_front_matter(raw)
    body = clean_markdown_body(raw_body)
    files = list_bundle_files(bundle_dir)
    title = as_text(original_metadata.get("title")) or bundle_dir.name
    date_value, lastmod_value, index_mtime = infer_datetime(index_path, original_metadata)

    excerpt = content_excerpt(body, files)
    metadata = ai_metadata(title, excerpt, collect_existing_tags())

    description = as_text(original_metadata.get("description")) or as_text(metadata["description"])
    categories = normalize_list(original_metadata.get("categories")) or normalize_list(metadata["categories"])
    tags = normalize_list(original_metadata.get("tags")) or normalize_list(metadata["tags"])

    generated_pages = write_markdown_attachment_pages(
        files, bundle_dir, title, date_value, lastmod_value, index_mtime
    )
    attachment_section = render_attachments(files, bundle_dir)
    sections = [body]
    if attachment_section:
        sections.append(attachment_section)
    output = (
        render_front_matter(title, description, date_value, lastmod_value, categories, tags)
        + "\n\n".join(section for section in sections if section.strip()).rstrip()
        + "\n"
    )
    index_path.write_text(output, encoding="utf-8")
    os.utime(index_path, (index_mtime.timestamp(), index_mtime.timestamp()))

    print(f"formatted {index_path.relative_to(REPO_ROOT)}")
    print("metadata_source=ai")
    print(f"model={DEEPSEEK_MODEL}")
    print(f"attachments={len(files)}")
    print(f"attachment_pages={len(generated_pages)}")
    print(f"date={date_value}")
    print(f"lastmod={lastmod_value}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
