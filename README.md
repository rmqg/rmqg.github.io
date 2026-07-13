# 若木秋光のBlog

Source repository for <https://blog.rmqg.org/>.

This site is built with Hugo and `hugo-theme-reimu`.

## 写文章

### 简单单语言文章

```bash
./scripts/new-post.sh "文章标题"
```

文件会创建为 `content/post/文章标题.md`，时间统一使用东八区。

### 图文或多语言文章

推荐使用 Hugo leaf bundle：

```bash
./scripts/new-post-bundle.sh "文章标题" "url-slug"
```

它会创建：

```text
content/post/url-slug/
└── index.md
```

图片、PDF 等附件直接放进同一目录，并在 `index.md` 中使用相对路径，例如：

```markdown
![截图](screenshot.png)
```

博客启用了四种语言。简体中文是 `index.md`，其余翻译分别命名为：

```text
index.en.md       # English
index.ja.md       # 日本語
index.zh-tw.md    # 繁體中文
```

四个文件应使用相同的 `date`，并各自翻译 `title`、`description`、分类、标签和正文。项目目前没有自动翻译脚本。

### 文章整理脚本

`content/post/format_blog_bundle.py` 只负责：

- 清理 Obsidian 嵌入语法；
- 为同目录附件生成链接或附件页面；
- 调用 DeepSeek 为简体中文 `index.md` 生成 description、分类和标签。

它**不会翻译文章**。使用方式：

```bash
export DEEPSEEK_API_KEY="你的密钥"
python3 content/post/format_blog_bundle.py "url-slug"
```

建议先写完并运行格式化脚本，再创建其他语言文件，避免翻译过程中中文源稿继续变化。

### 本地预览

```bash
hugo server -D
```

发布前构建：

```bash
hugo --gc --minify --baseURL "https://blog.rmqg.org/"
```

推送到 `main` 后，GitHub Actions 会自动构建并部署到 GitHub Pages。

## License

Original site content, site-specific code, configuration modifications, and authorized friend-link entries are distributed under the GNU General Public License v3.0.

Third-party template, theme, and asset material keeps its original licensing status. See [NOTICE](NOTICE) for details.
