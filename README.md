# 若木秋光のBlog

Source repository for <https://blog.rmqg.org/>.

This site is built with Hugo and `hugo-theme-reimu`.

## 使用博客工具

需要 Python 3.9+、PyYAML 和 Hugo。安装 Python 依赖后运行统一菜单：

```bash
python3 -m pip install PyYAML
python3 scripts/blog.py
```

按数字选择「新建文章」「新建碎记」「整理/翻译」「本地预览」或「退出」。最简单的流程：

1. 选 1 或 2 新建草稿，按提示填标题，目录名可直接回车。
2. 打开终端显示的 `index.md` 写正文，图片、PDF 等附件放在同一目录。
3. 写完选 3，选文章编号并确认：AI 生成摘要、分类和标签，整理格式并更新三种翻译。
4. 要发布时将 `draft: true` 改为 `draft: false`，再运行选项 3，同步各语言的发布状态。

整理可选单页或全部，会提示确认覆盖已有翻译。`date` 保留首次发表时间，`lastmod` 更新为本次整理时间；全部时间采用 `+08:00`，四语言同步。分类/标签按正文生成并优先复用站内名称，不再给每篇新稿固定套用「随笔/随想」。独立页面不强行添加文章分类。

日期、更新日期和阅读时间在窄屏自动换行，避免同步更新时间后撑宽手机页面。

新稿均为 leaf bundle。四语言文件为 `index.md`、`index.en.md`、`index.ja.md`、`index.zh-tw.md`，普通页面使用相同语言后缀。预览按 Ctrl+C 返回菜单。

整理/翻译使用 OpenAI 兼容 API：优先读取 `OPENAI_API_KEY`、`OPENAI_BASE_URL`、`OPENAI_MODEL` 环境变量，其次读取根目录 `.blog-api.json`（`base_url`、`api_key`、`model`），最后在终端安全提示输入 API Key。默认地址为 `https://edge.gpt.rmqg.org/v1`，模型为 `gemini-3.8-flash`。脚本只整理本地文件，不发布或推送。

`.blog-api.json` 已被 `.gitignore` 排除，含密钥，勿上传或分享。环境变量可覆盖本地配置。翻译需联网；已有中文正文、发表日期、发布状态、代码、HTML/CSS、shortcode 与附件地址均保留。

## License

Original site content, site-specific code, configuration modifications, and authorized friend-link entries are distributed under the GNU General Public License v3.0.

Third-party template, theme, and asset material keeps its original licensing status. See [NOTICE](NOTICE) for details.
