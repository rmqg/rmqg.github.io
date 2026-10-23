#!/usr/bin/env python3
"""Interactive Hugo blog authoring, cleanup, and translation helper."""
from __future__ import annotations

import datetime as dt
import getpass
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

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
POSTS = CONTENT / "post"
TZ = dt.timezone(dt.timedelta(hours=8))
LANGUAGES = {"en": "English", "ja": "Japanese", "zh-tw": "Traditional Chinese"}
IMAGE_EXTS = {".avif", ".gif", ".jpeg", ".jpg", ".png", ".svg", ".webp"}
TEXT_EXTS = {".csv", ".log", ".txt"}
FM_RE = re.compile(r"\A(---|\+\++)\s*\n(.*?)\n\1\s*(?:\n|\Z)", re.S)
OBSIDIAN_RE = re.compile(r"!\[\[([^\]]+)\]\]")
INDEX_RE = re.compile(r"^index(?:\.[A-Za-z-]+)?\.md$")


def ask(prompt: str, default: str = "") -> str:
    try:
        value = input(f"{prompt}{f' [{default}]' if default else ''}: ").strip()
        return value or default
    except (EOFError, KeyboardInterrupt):
        print("\n已取消。")
        raise


def timestamp() -> str:
    return dt.datetime.now(TZ).replace(microsecond=0).isoformat()


def safe_component(value: str) -> str:
    value = value.strip().strip("/\\")
    if not value or value in {".", ".."} or Path(value).name != value:
        raise ValueError("名称不能为空，且不能包含路径分隔符。")
    return value


def create_post() -> None:
    title = ask("文章标题")
    if not title:
        print("标题不能为空；未创建文章。")
        return
    slug = safe_component(ask("目录名/slug（留空使用标题）", title))
    bundle = POSTS / slug
    if bundle.exists():
        print(f"已存在，不覆盖：{bundle}")
        return
    now = timestamp()
    bundle.mkdir(parents=True)
    target = bundle / "index.md"
    try:
        with target.open("x", encoding="utf-8") as f:
            f.write(f"---\ntitle: {json.dumps(title, ensure_ascii=False)}\ndescription: {json.dumps(title, ensure_ascii=False)}\ndate: {now}\nlastmod: {now}\ndraft: true\n---\n\n")
    except BaseException:
        try: bundle.rmdir()
        except OSError: pass
        raise
    print(f"已创建草稿：{target.relative_to(ROOT)}")


def create_note() -> None:
    title = ask("碎记标题（留空为无标题碎记）")
    default = dt.datetime.now(TZ).strftime("%Y-%m-%d-%H%M%S")
    slug = safe_component(ask("中文目录名/slug", title or default))
    bundle = CONTENT / "notes" / slug
    if bundle.exists():
        print(f"已存在，不覆盖：{bundle}")
        return
    now = timestamp()
    bundle.mkdir(parents=True)
    target = bundle / "index.md"
    try:
        with target.open("x", encoding="utf-8") as f:
            f.write(f"---\ntitle: {json.dumps(title or dt.datetime.now(TZ).strftime('%Y-%m-%d 碎记'), ensure_ascii=False)}\ndate: {now}\nlastmod: {now}\ndraft: true\nshowTitle: {str(bool(title)).lower()}\n---\n\n")
    except BaseException:
        try: bundle.rmdir()
        except OSError: pass
        raise
    print(f"已创建碎记草稿：{target.relative_to(ROOT)}")


def split_front(text: str) -> tuple[str, str, str]:
    m = FM_RE.match(text)
    if not m: return "", "", text
    return m.group(1), m.group(2), text[m.end():]


class ContentDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def parse_meta(raw: str) -> dict[str, object]:
    metadata = yaml.safe_load(raw) or {}
    if not isinstance(metadata, dict):
        raise ValueError("Front matter 必须是 YAML 对象。")
    return metadata


def listval(value: object) -> list[str]:
    if isinstance(value, list): return [str(x).strip() for x in value if str(x).strip()]
    return [value.strip()] if isinstance(value, str) and value.strip() else []


def clean_body(body: str) -> str:
    """Convert embeds outside fences without discarding user attachment sections."""
    lines = []
    fence = None
    for line in body.replace("\r\n", "\n").replace("\r", "\n").splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            lines.append(line)
            continue
        if fence:
            lines.append(line)
            continue
        def conv(match: re.Match[str]) -> str:
            target = match.group(1).split("|", 1)[0].strip()
            label = Path(target).stem
            return f"![{label}](<{target}>)" if Path(target).suffix.lower() in IMAGE_EXTS else f"[{label}](<{target}>)"
        lines.append(OBSIDIAN_RE.sub(conv, line))
    return "\n".join(lines).strip()


def bundle_files(bundle: Path) -> list[Path]:
    files=[p for p in bundle.iterdir() if p.is_file() and not INDEX_RE.match(p.name) and not p.name.startswith(".")]
    return sorted(files,key=lambda p:(0 if p.suffix.lower()==".md" else 1 if p.suffix.lower()==".pdf" else 2 if p.suffix.lower() in IMAGE_EXTS else 3 if p.suffix.lower() in TEXT_EXTS else 4,p.name.casefold()))


def file_title(path: Path) -> str:
    if path.suffix.lower()==".md":
        _,_,body=split_front(path.read_text(encoding="utf-8"))
        for line in body.splitlines():
            m=re.match(r"^\s*#\s+(.+?)\s*$",line)
            if m:return m.group(1)
    return path.stem


def metadata_ai(title: str, excerpt: str, tags: list[str], cfg: dict[str,str]) -> dict[str,object]:
    categories = set()
    for path in collect_docs():
        categories.update(listval(parse_meta(split_front(path.read_text(encoding="utf-8"))[1]).get("categories")))
    prompt = {"title": title, "content": excerpt, "existing_tags": tags, "existing_categories": sorted(categories),
              "rules": ["Return strict JSON only.", "Faithful Chinese description under 60 Chinese characters; do not invent facts.",
                        "Use 1 or 2 broad Chinese categories and 2 to 5 specific tags (1 tag is enough for a very short note).",
                        "Reuse an existing label when it means the same thing; avoid synonyms, vague filler and excessive labels."],
              "schema": {"description": "string", "categories": ["string"], "tags": ["string"]}}
    raw = api_call(cfg, [{"role": "system", "content": "Choose accurate, consistent metadata for a Chinese personal blog. Return JSON only."}, {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)}])
    result = json.loads(re.sub(r"\A```(?:json)?\s*|\s*```\Z", "", raw.strip()))
    if not isinstance(result.get("description"), str) or not result["description"].strip():
        raise RuntimeError("AI 未返回有效摘要，原文未修改。")
    for key, maximum in (("categories", 2), ("tags", 5)):
        values = result.get(key)
        if not isinstance(values, list) or not values or len(values) > maximum or any(not isinstance(v, str) or not v.strip() for v in values):
            raise RuntimeError(f"AI 返回的 {key} 无效，原文未修改。")
        result[key] = list(dict.fromkeys(v.strip() for v in values))
    return result


def credentials() -> dict[str,str]:
    config={}
    path=ROOT/".blog-api.json"
    if path.is_file():
        try: config=json.loads(path.read_text(encoding="utf-8"))
        except (OSError,json.JSONDecodeError) as e: print(f"忽略无效 .blog-api.json：{e}",file=sys.stderr)
    base=os.environ.get("OPENAI_BASE_URL") or config.get("base_url") or "https://edge.gpt.rmqg.org/v1"
    key=os.environ.get("OPENAI_API_KEY") or config.get("api_key") or ""
    model=os.environ.get("OPENAI_MODEL") or config.get("model") or "gemini-3.8-flash"
    if not key:
        key=getpass.getpass("OpenAI兼容 API Key（输入不回显）: ").strip()
    if not key: raise RuntimeError("未提供 API key")
    return {"base_url":str(base).rstrip("/"),"api_key":str(key),"model":str(model)}


def api_call(cfg: dict[str,str], messages: list[dict[str,str]], json_mode: bool=False) -> str:
    payload={"model":cfg["model"],"messages":messages,"temperature":0.2,"max_tokens":16000}
    if json_mode: payload["response_format"]={"type":"json_object"}
    req=urllib.request.Request(cfg["base_url"]+"/chat/completions",data=json.dumps(payload,ensure_ascii=False).encode(),headers={"Authorization":"Bearer "+cfg["api_key"],"Content-Type":"application/json"},method="POST")
    try:
        with urllib.request.urlopen(req,timeout=120) as response: result=json.loads(response.read().decode())
    except (OSError,urllib.error.URLError,json.JSONDecodeError) as e: raise RuntimeError(f"API请求失败：{e}") from e
    try:
        choice = result["choices"][0]
        if choice.get("finish_reason") != "stop":
            raise RuntimeError("API 未完整返回；未写入翻译，请重试。")
        return choice["message"]["content"].strip()
    except (KeyError, IndexError, TypeError, AttributeError) as e:
        raise RuntimeError("API 响应缺少有效正文。") from e


def translate(source: str, lang: str, cfg: dict[str, str]) -> str:
    _, raw_meta, body = split_front(source)
    meta = parse_meta(raw_meta)
    pattern = re.compile(r"(?ms)^(`{3,}|~{3,})[^\n]*\n.*?^\1[^\n]*(?:\n|$)|<style\b[^>]*>.*?</style>|<!--.*?-->|\{\{[<%].*?[%>]\}\}|<[^>]+>")
    protected = []
    def hide(match):
        protected.append(match.group(0))
        return f"BLOG_PROTECTED_{len(protected) - 1:04d}"
    masked = pattern.sub(hide, body)
    fields = {k: meta[k] for k in ("title", "description", "categories", "tags") if k in meta}
    fields["body"] = masked
    instruction = (f"Translate every prose value into {LANGUAGES[lang]}. Return only JSON with exactly the input keys and types. "
                   "Preserve meaning, informal tone, Markdown, URLs, filenames, inline code and BLOG_PROTECTED_NNNN placeholders. "
                   "Do not summarize or invent facts. Keep the display name 若木秋光 unchanged.")
    raw = api_call(cfg, [{"role": "system", "content": instruction}, {"role": "user", "content": json.dumps(fields, ensure_ascii=False)}])
    raw = re.sub(r"\A```(?:json)?\s*|\s*```\Z", "", raw.strip())
    result = json.loads(raw)
    if not isinstance(result, dict) or any(k not in result or type(result[k]) is not type(v) for k, v in fields.items()):
        raise RuntimeError("翻译字段不完整或类型错误，未保存。")
    translated = result["body"]
    for i, block in enumerate(protected):
        token = f"BLOG_PROTECTED_{i:04d}"
        if translated.count(token) != masked.count(token):
            raise RuntimeError("翻译改变了受保护内容，未保存。")
        translated = translated.replace(token, block)
    for key in fields:
        if key != "body":
            meta[key] = result[key]
    return "---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False, width=1000) + "---\n\n" + translated.strip() + "\n"


def translate_docs(docs: list[Path], cfg: dict[str, str]) -> None:
    label_cache = {lang: {} for lang in LANGUAGES}
    for path in docs:
        text = path.read_text(encoding="utf-8")
        source_meta = parse_meta(split_front(text)[1])
        for lang in LANGUAGES:
            target = path.with_name(path.stem + f".{lang}.md")
            result = translate(text, lang, cfg)
            if path.read_text(encoding="utf-8") != text:
                raise RuntimeError(f"源稿已修改，未保存旧翻译：{path.relative_to(ROOT)}")
            _, raw_meta, body = split_front(result)
            metadata = parse_meta(raw_meta)
            for field in ("categories", "tags"):
                originals = listval(source_meta.get(field))
                translated_labels = listval(metadata.get(field))
                if len(originals) != len(translated_labels):
                    raise RuntimeError("翻译改变了分类或标签数量，未保存。")
                if originals:
                    metadata[field] = [label_cache[lang].setdefault(label, translated_label) for label, translated_label in zip(originals, translated_labels)]
            target.write_text(render_document(metadata, body), encoding="utf-8")
            print(f"已同步：{target.relative_to(ROOT)}")


def collect_docs() -> list[Path]:
    docs = []
    for path in sorted(CONTENT.rglob("*.md")):
        if any(path.stem.endswith("." + lang) for lang in LANGUAGES):
            continue
        if path.parent == CONTENT or path.name in {"index.md", "_index.md"} or path.parent.name in {"notes", "post"}:
            docs.append(path)
    return docs


def choose_docs() -> list[Path]:
    docs=collect_docs()
    if not docs: print("没有找到可整理/翻译的中文源稿。"); return []
    print("源稿：")
    for i,p in enumerate(docs,1): print(f"{i}. {p.relative_to(ROOT)}")
    choice=ask("输入编号整理单页，或 a 处理全部", "a").lower()
    if choice in {"a","all","全部"}: return docs
    try: index=int(choice)-1
    except ValueError: print("输入无效，未处理。"); return []
    if not 0<=index<len(docs): print("编号超出范围，未处理。"); return []
    return [docs[index]]


def format_post(index: Path, cfg: dict[str, str]) -> None:
    bundle = index.parent
    delimiter, raw_meta, raw_body = split_front(index.read_text(encoding="utf-8"))
    if delimiter not in {"", "---"}:
        raise ValueError("整理功能仅支持 YAML front matter；原文未改动。")
    meta = parse_meta(raw_meta)
    body = clean_body(raw_body)
    title = str(meta.get("title") or bundle.name)
    meta.setdefault("title", title)
    # Metadata is generated once in organize_docs; this function handles attachments.
    if "date" not in meta:
        raise ValueError("缺少发表日期，请先填写 date；不会用文件修改时间猜测。")
    additions = []
    for attachment in bundle_files(bundle):
        relative = attachment.name
        # Preserve authored links/embeds and append only genuinely unreferenced files.
        if relative in body or urllib.parse.quote(relative) in body:
            continue
        if attachment.suffix.lower() == ".md":
            page_slug = urllib.parse.quote(bundle.name + "-" + attachment.stem)
            if "/post/" + page_slug + "/" in body:
                continue
            page = POSTS / (bundle.name + "-" + attachment.stem) / "index.md"
            if not page.exists():
                page.parent.mkdir(parents=True, exist_ok=True)
                attachment_meta = {k: meta[k] for k in ("date", "lastmod", "draft") if k in meta}
                attachment_meta["title"] = file_title(attachment)
                page.write_text("---\n" + yaml.safe_dump(attachment_meta, allow_unicode=True, sort_keys=False) + "---\n\n" + split_front(attachment.read_text(encoding="utf-8"))[2].strip() + "\n", encoding="utf-8")
            additions.append(f"- [{file_title(attachment)}](</post/{urllib.parse.quote(page.parent.name)}/>)")
        elif attachment.suffix.lower() in IMAGE_EXTS:
            additions.append(f"![{file_title(attachment)}](<{relative}>)")
        else:
            additions.append(f"- [{relative}](<{relative}>)")
    if additions:
        body += ("\n\n" if "## 附件" in body else "\n\n## 附件\n\n") + "\n\n".join(additions)
    output = render_document(meta, body)
    index.write_text(output, encoding="utf-8")
    print(f"已整理：{index.relative_to(ROOT)}")


def format_body(body: str) -> str:
    """Normalize prose spacing without editing fenced code or HTML blocks."""
    output = []
    fence = None
    html = None
    for line in clean_body(body).splitlines():
        stripped = line.strip()
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            output.append(line)
            continue
        if fence:
            output.append(line)
            continue
        if re.match(r"<(style|script)\b", stripped):
            html = stripped.split(">", 1)[0].split()[0][1:]
        if html:
            output.append(line)
            if f"</{html}>" in line:
                html = None
            continue
        if re.match(r"^#{1,6}\s", line):
            if output and output[-1]:
                output.append("")
            output.extend([line.rstrip(), ""])
        elif stripped or not output or output[-1]:
            output.append(line.rstrip())
    return "\n".join(output).strip() + "\n"


def render_document(meta: dict[str, object], body: str) -> str:
    preferred = ("title", "description", "date", "lastmod", "draft", "showTitle", "slug", "url", "aliases", "categories", "tags")
    ordered = {key: meta[key] for key in preferred if key in meta}
    ordered.update({key: value for key, value in meta.items() if key not in ordered})
    for key in ("date", "lastmod"):
        if key not in ordered:
            continue
        value = ordered[key]
        if isinstance(value, str):
            value = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
            value = dt.datetime.combine(value, dt.time())
        if value.tzinfo is None:
            value = value.replace(tzinfo=TZ)
        ordered[key] = value.astimezone(TZ).replace(microsecond=0).isoformat()
    raw = yaml.dump(ordered, Dumper=ContentDumper, allow_unicode=True, sort_keys=False, width=1000)
    raw = re.sub(r"^(date|lastmod): ['\"]([^'\"]+)['\"]$", r"\1: \2", raw, flags=re.M)
    raw = re.sub(r"^(date|categories):", r"\n\1:", raw, flags=re.M)
    return "---\n" + raw + "---\n\n" + format_body(body)


def organize_docs(docs: list[Path], cfg: dict[str, str]) -> None:
    updated = timestamp()
    tags = set()
    for source in collect_docs():
        tags.update(listval(parse_meta(split_front(source.read_text(encoding="utf-8"))[1]).get("tags")))
    for path in docs:
        delimiter, raw_meta, body = split_front(path.read_text(encoding="utf-8"))
        if delimiter != "---":
            raise ValueError(f"请先为 {path.name} 添加 YAML front matter。")
        meta = parse_meta(raw_meta)
        article = path.name != "_index.md" and path.is_relative_to(CONTENT) and path.relative_to(CONTENT).parts[0] in {"post", "notes"}
        if article:
            if "date" not in meta:
                raise ValueError(f"{path.name} 缺少发表日期，请先填写 date。")
            generated = metadata_ai(str(meta.get("title") or path.parent.name), body, sorted(tags), cfg)
            meta.update({key: generated[key] for key in ("description", "categories", "tags")})
            tags.update(generated["tags"])
        meta["lastmod"] = updated
        path.write_text(render_document(meta, body), encoding="utf-8")
        if path.is_relative_to(POSTS) and path.name == "index.md":
            format_post(path, cfg)
    translate_docs(docs, cfg)


def preview() -> None:
    print("启动 Hugo 本地预览（Ctrl+C 返回菜单）…")
    try: subprocess.run(["hugo","server","-D"],cwd=ROOT,check=False)
    except FileNotFoundError: print("未找到 hugo，请先安装 Hugo。")


def main() -> int:
    while True:
        print("\n博客工具\n1. 新建文章\n2. 新建碎记\n3. 整理/翻译已有内容\n4. 本地预览\n5. 退出")
        try: choice=ask("请选择", "5")
        except (EOFError,KeyboardInterrupt): return 0
        try:
            if choice=="1": create_post()
            elif choice=="2": create_note()
            elif choice=="3":
                docs=choose_docs()
                if docs and ask("将用 AI 更新分类/标签并覆盖三语翻译，继续？", "y").lower() == "y":
                    organize_docs(docs, credentials())
            elif choice=="4": preview()
            elif choice=="5": return 0
            else: print("请输入 1–5。")
        except (KeyboardInterrupt,EOFError): print("\n已取消当前操作。")
        except (OSError, ValueError, RuntimeError, yaml.YAMLError) as e: print(f"操作失败：{e}",file=sys.stderr)
    return 0

if __name__=="__main__": raise SystemExit(main())
