#!/bin/bash
set -euo pipefail

title="${1:-}"
slug="${2:-}"
if [ -z "$title" ]; then
    read -r -p "文章标题: " title
fi
if [ -z "$slug" ]; then
    slug=$(printf '%s' "$title" | tr ' ' '-')
fi

now=$(TZ=Asia/Shanghai date +"%Y-%m-%dT%H:%M:%S+08:00")
bundle="content/post/${slug}"
file="${bundle}/index.md"
if [ -e "$file" ]; then
    echo "文件已存在: $file" >&2
    exit 1
fi

mkdir -p "$bundle"
cat > "$file" <<EOF
---
title: ${title}
description: ${title}

date: ${now}
lastmod: ${now}

categories:
  - 随笔
tags:
  - 随想
---

EOF

echo "已创建: $file"
echo "多语言文件命名: index.en.md / index.ja.md / index.zh-tw.md"
