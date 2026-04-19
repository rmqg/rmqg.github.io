#!/bin/bash
title="${*:-}"
if [ -z "$title" ]; then
    read -p "文章标题: " title
fi
now=$(date +"%Y-%m-%dT%H:%M:%S+08:00")
slug=$(echo "$title" | tr ' ' '-')
file="content/post/${slug}.md"
cat > "$file" <<EOF
---
title: ${title}
description: ${title}

date: ${now}
lastmod: ${now}
---

EOF
echo "已创建: $file"
