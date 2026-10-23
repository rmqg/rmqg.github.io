---
description: A detailed record of the third-generation blog's complete setup process, from local debugging, Hugo theme configuration, and GitHub Actions automated deployment, to connecting a custom domain, Dogecloud CDN acceleration, and COS object storage, with the complete workflow code included.

date: 2026-04-19T11:58:32+08:00
lastmod: 2026-10-23T21:51:19+08:00

categories:
  - Tech
  - Tinkering
tags:
  - Blog
  - Hugo
  - GitHub Actions
  - CDN
---

title: Notes on Building My Blog for the Third Time
description: Notes on Building My Blog for the Third Time

date: 2026-04-19T11:58:32+08:00
lastmod: 2026-04-19T20:52:06+08:00
---

## Preface

Partly to have something to talk about during my cybersecurity transfer interview, I decided to revive this blog that I hadn't maintained in a long time. Since I'm also fairly lazy by nature, if I built it the same way as the previous two generations — `WordPress+MySql+PHP` — there was a real chance I'd lose all the data from neglecting server maintenance. Deploying Blog Very.3.0 on `Github Pages` handles this problem nicely: even if I slack off on maintenance, all posts, comments, and everything else will remain in the Github repository, with no risk of losing anything to an expired server.

So I built this blog using the `Hugo+Github Actions` combination, with the anime-style theme `hugo-theme-reimu` recommended by Claude Sonnet 4.6.

{{<link title="HUGO" link="https://gohugo.io" cover="https://github.com/gohugoio/hugo/blob/master/docs/static/apple-touch-icon.png?raw=true">}}

{{<link title="hugo-theme-reimu" link="https://github.com/D-Sketon/hugo-theme-reimu" cover="https://camo.githubusercontent.com/66beeb49b45f16c66f7df739279b5da72a453aa5dd3c91730c5a39fe20eee15d/68747470733a2f2f666173746c792e6a7364656c6976722e6e65742f67682f442d536b65746f6e2f626c6f672d696d672f69636f6e2e706e67">}}

All files for this blog are stored in the Republic Repository: [https://github.com/rmqg/rmqg.github.io](https://github.com/rmqg/rmqg.github.io), which readers are welcome to browse as a reference.

## Step 1: Local Development and Testing

I noticed that `D-Sketon`, the author of `hugo-theme-reimu`, states in the project's readme:

> [!NOTE]
> Complete beginners can use `hugo-reimu-template` directly. Just clone the repository and modify the configuration to get a basic blog up and running!

I tried following the standard setup process step by step, gave up after a short while, forked the entire template project, and used that as my starting point instead — saving myself a lot of unnecessary hassle. (The template project offers the same degree of customisability as the standard process; `D-Sketon` has simply taken care of a lot of the default configuration for you.)

{{<link title="hugo-reimu-template" link="https://github.com/D-Sketon/hugo-reimu-template" cover="https://camo.githubusercontent.com/66beeb49b45f16c66f7df739279b5da72a453aa5dd3c91730c5a39fe20eee15d/68747470733a2f2f666173746c792e6a7364656c6976722e6e65742f67682f442d536b65746f6e2f626c6f672d696d672f69636f6e2e706e67">}}

After forking the template repository and pulling it to my development machine, I followed the `hugo-theme-reimu` project's tutorial: first editing `hugo.toml` to complete the basic configuration, then working through `config/_default/params.yml` from top to bottom to customise the template to my liking. ~~(Whenever I hit a configuration option I didn't understand, I just asked an AI.)~~

The changes to `params.yml` were quite extensive — I worked through every line from top to bottom. The following records all the changes I made, in file order. ~~(Should be all of them, with nothing missed.)~~

### Basic Information and Subtitle

First I updated the `author`, `email`, and `description` fields with my own information.

`hugo-theme-reimu` supports a typewriter animation effect for the subtitle, which can be configured under `subtitle.typing`:

```yaml
subtitle:
  typing:
    enable: true
    strings:
      - "若木秋光のBlog へようこそ！"
      - "ここから、始めましょう。一から…いいえ、ゼロから！"
      - "さあ、ゲームを始めよう。"
    typeSpeed: 100
    backSpeed: 50
    backDelay: 2000
```

The three strings cycle through, each being typed out and then deleted. The default speed settings produce a nice effect. The `text` field serves as a static fallback when `typing.enable: false`, and I updated that as well.

I also enabled `banner_srcset` to configure Banner images at different resolutions so that smaller versions load on mobile. I changed `excerpt_link` to `继续阅读` ("Continue Reading"), which fits better with the blog's primarily Chinese content.

### Footer and Social Links

I set `footer.since` to `2026` to reflect the actual start year, and set `powered` to `false` to remove the "Powered by Hugo" text.

Under the `social` field I filled in links for various platforms; the theme automatically renders the corresponding icons in the sidebar. I added `email`, `github`, `bilibili`, `telegram`, `steam`, as well as `qq` and `weixin` (since Tencent, in their infinite wisdom, provides no API for these, I had to save friend-request QR codes locally and reference them that way). `网易云音乐` (NetEase Cloud Music) isn't in the theme's built-in icon list, so it needs to be handled separately via `injector` later (the CSS editing for that section was done by —). For now I just put a placeholder link here.

### Showing Last-Updated Time and Corner Badge

I set `show_update_time` to `true` so that the last-modified time is shown on both the post list and post detail pages. I also enabled `triangle_badge`, chose `github` as the icon, and set the link to my own profile page — this adds a small badge in the top-right corner of the page pointing to my Github homepage.

### Fonts

I changed the body font from `Noto Serif SC` (a serif font, similar to Song typeface) to `Noto Sans SC` (a sans-serif font, similar to Hei typeface), and added `JetBrains Mono` as a code font (because I find the original font uncomfortable to read on screen):

```yaml
font:
  enable: true
  article:
    - Mulish
    - Noto Sans SC
  code:
    - JetBrains Mono
```

All of the above fonts are hosted on Google Fonts and are loaded automatically by the theme — no extra configuration needed.

### Miscellaneous Feature Toggles

I set `mermaid.zoom` to `true` so that diagrams support mouse-wheel zooming. I filled in `clipboard.copyright.content` with a copyright notice that gets automatically appended when more than a certain number of characters are copied. (I later discovered this feature only works on the copy button in code blocks, so I disabled it in a subsequent edit.)

### Comment System

I changed `comment.default` from `waline` to `giscus`, then filled in the repository configuration generated from [giscus.app](https://giscus.app/zh-CN) under the `giscus` field:

```yaml
giscus:
  enable: true
  repo: rmqg/rmqg.github.io
  repoId: R_kgDOSFIuEQ
  category: Announcements
  categoryId: DIC_kwDOSFIuEc4C7HRY
  mapping: pathname
  theme:
    light: light
    dark: dark
```

`giscus` is built on top of `GitHub Discussions`, so comment data is stored in the repository itself. There's no risk of a third-party service disappearing, and it aligns perfectly with the goal of this version of the blog: low-maintenance and hassle-free.

### Preloader, Copyright Notice, Sponsorship, and Sharing

I changed the loading text for each language in `preloader` to phrases that echo the subtitle.

I enabled `article_copyright` and configured it to display the author, title, date, last-updated time, and licence. I chose `by-nc-sa` as the licence type.

I filled in `moe_icp.icpnumber` with my Moe ICP registration number (just the numeric part).

I enabled `sponsor` and placed the Alipay and WeChat payment QR codes in the `static/sponsor/` directory, then set the `qr` field to the corresponding paths.

For the `share` field I uncommented all the commonly used platforms, so a share bar will appear at the bottom of each post.

I added a placeholder test category in `home_categories` for now; I'll organise things properly once there are more posts.

### Code Injection (injector)

This is the most miscellaneous section of changes. Three pieces of content were injected into `injector.head_end`:
- NetEase Cloud Music icon CSS (using `mask` + SVG to cut out the icon shape, with `currentColor` inheriting the colour for light/dark mode compatibility)
- Minor style tweaks for APlayer's fixed positioning, plus a Live2d model ID initialisation script (to pin a specific model and prevent it from randomly changing on every page refresh)
- A patch injected into `injector.body_end` to fix the missing loop-button SVG in MetingJS when loading from the cloud, resolving the issue of the loop icon disappearing during Meting's remote load.

~~(Basically all the CSS and JS in the injector was written by Claude Sonnet 4.6 — I couldn't make sense of it myself.)~~

### PJAX, Live2d, and the Music Player

I set `pjax.enable` to `true` so that page navigation becomes a partial refresh, making transitions faster and preventing the music player from being interrupted when navigating between pages. I set `live2d_widgets.enable` to `true` so that the mascot character appears in the bottom-left corner of the page.

For the music player, I enabled `aplayer` and configured autoplay (though it doesn't actually trigger in practice due to browser restrictions), shuffle order, volume at 0.3, and list-loop mode. I then enabled `meting` and filled in the NetEase Cloud Music playlist ID along with a custom API address. (I originally set up an API on Vercel using my own cookie, but when I was later optimising connection latency I found this had become the bottleneck, so I switched to the API maintained by `injahow` themselves.) (The API call syntax here should be updated — the original form throws an error.):

```yaml
meting:
  enable: true
  meting_api: "https://api.injahow.cn/meting/?server=:server&type=:type&id=:id&r=:r"
  options:
    id: 17883899120
    server: netease
    type: playlist
```

I set `pangu.enable` to `true` to automatically insert spaces between Chinese and English text. ~~(Because I have severe OCD.)~~

### Theme Colour and Dynamic Colour Scheme

The original `hugo-theme-reimu` uses a red colour scheme, but I prefer blue, so I replaced all the `--red-*` variables under `internal_theme` with blue values — one set for light mode and one for dark mode. ~~(All the colour codes were generated by Claude Sonnet 4.6.)~~ The variable names are called `--red-*` simply because that's the placeholder naming convention in the theme; the actual colour is whatever value you assign.

I later enabled `material_theme`, which automatically extracts the dominant colour from the Banner image to generate a dynamic colour scheme. This makes the overall look much more cohesive with the Banner. ~~(As a result, most of the colours I set manually got overridden anyway.)~~

### Summary

Throughout all of the above, I ran `hugo server` locally to preview and tweak things repeatedly, occasionally pushing to Github to preview there as well, until I was satisfied with the result.

The overall configuration process isn't very intuitive without a GUI, but the logic is straightforward and easy to follow, making it reasonably simple to set up. ~~(Is this one of the advantages of projects developed by Chinese developers?)~~

> [!CAUTION]
> When modifying any files, do **not** make changes inside the `themes/hugo-theme-reimu` folder — doing so will cause headaches with `Git`. Instead, refer to the file's location within `themes/hugo-theme-reimu`, create a matching folder structure inside your own configuration directory, copy the file you want to modify into it, and then make your changes there.

## Step 2: Deploying to Github Pages

This step sets up `Github Actions` to automatically build the Hugo site and deploy it to `Github Pages` on every push, eliminating the need for any manual steps.

`hugo-reimu-template` doesn't include a workflow file out of the box, so you need to create one yourself under `.github/workflows/`.

The entire workflow is split into two jobs: `build` handles installing Hugo, building the site, and uploading the build artefact; `deploy` depends on `build` completing successfully and then publishes the artefact to `Github Pages`.

There are a few details worth noting in the `build` job:

- `submodules: recursive` is added to the `checkout` step because the theme is included as a Git submodule — without this parameter, the theme files won't be pulled down.
- `fetch-depth: 0` tells Git to fetch the full commit history, which Hugo needs in order to correctly generate `lastmod` timestamps for posts.
- Hugo must be installed in its `Extended` edition to support Sass/SCSS. You can download and extract it directly from a GitHub Release and add it to `PATH`.

```yaml
name: 构建并部署 Hugo 博客

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      HUGO_VERSION: 0.160.0
    steps:
      - name: 拉取代码
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: 安装 Hugo Extended
        run: |
          curl -sLJO "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
          mkdir -p ~/.local/hugo
          tar -C ~/.local/hugo -xf "hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
          echo "$HOME/.local/hugo" >> $GITHUB_PATH

      - name: 配置 Pages
        id: pages
        uses: actions/configure-pages@v5

      - name: 构建站点
        run: hugo --gc --minify

      - name: 上传构建产物到github
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: 部署到 GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

Once the workflow file is written, you also need to go to the repository's `Settings → Pages` and change `Source` to `Github Actions` — otherwise deployments will fail silently with no error message whatsoever.

I ran into one gotcha along the way: I originally wrote the build command as `hugo --gc --minify --baseURL "${{ steps.pages.outputs.base_url }}/"`, intending to let the `configure-pages` action pass in the `baseURL` dynamically. The problem was that it passed in an `http://`-prefixed address, which caused all absolute links in the generated HTML to be HTTP — resulting in mixed content errors across the board in an HTTPS-enforced environment. The fix was to remove the `--baseURL` flag from the build command entirely and hard-code `baseURL = 'https://blog.rmqg.org/'` directly in `hugo.toml`. Problem solved. ~~(Took me quite a while to track that one down.)~~

## Step 3: Writing the "About" and "Friends" Pages

This step simply involves writing the two files `content/friend.md` and `content/about.md` and filling them with your own content. You can also create additional files such as `content/about.en.md`, `content/about.ja.md`, and `content/about.zh-tw.md` so that switching the language in the top-right corner of the page shows the corresponding language version of the `About` page and similar pages. (I used Claude Sonnet 4.6 to translate the non-Chinese language versions.)

## Step 4: Connecting a Custom Domain

Everything up to this point was running under Github's domain `https://rmqg.github.io/`. The steps that follow involve pointing a custom domain at the blog and optimising connection performance.

### Binding a Custom Domain

First, go to the Github repository's `Settings → Pages → Custom domain`, enter `blog.rmqg.org`, and save. Github will automatically create a `CNAME` file in the root of the repository (containing just the single line `blog.rmqg.org`) and immediately trigger a build and deployment to include that file. (During final testing I noticed that visiting `rmqg.github.io` actually redirects to `rmqg.org` — apparently because the browser had cached an old DNS resolution. Opening an incognito window resolved the issue.)

The domain is hosted on `CloudFlare`. In the DNS panel, add a `CNAME` record: set the name to `blog`, the target to `rmqg.github.io`, and leave the cloud icon on the right **grey** (i.e. Proxied disabled, DNS-only mode). Save and wait for DNS propagation — typically anywhere from a few minutes to half an hour — after which `blog.rmqg.org` will be accessible.

> [!TIP]
> Once a custom domain is bound, visiting `rmqg.github.io` will be automatically 302-redirected by Github to `blog.rmqg.org`. This is built-in Github Pages behaviour and has nothing to do with CloudFlare — no separate redirect rules need to be configured.

Back in the Github Pages settings, once Github detects that DNS is resolving correctly, tick `Enforce HTTPS`. Github will automatically obtain a certificate via Let's Encrypt and renew it before it expires. Note, however, that this certificate is managed by Github — the private key is not in your hands and cannot be exported. Keep this in mind when setting up a CDN later.

> [!NOTE]
> If you find the `Enforce HTTPS` option is greyed out immediately after binding the domain, just wait a few minutes for Github to finish issuing the certificate, and it will become available.

### Considering CloudFlare's Orange Cloud for Acceleration

My initial plan was to simply enable CloudFlare's orange cloud and let CF's CDN proxy all traffic. After testing, I found that this route was very slow for visitors in China — the first page load took tens of seconds and some CSS failed to render entirely. So I went looking for an alternative.

CloudFlare remains on grey cloud (DNS only) throughout; the acceleration task is handed off to a domestic CDN instead.

### Discovering the Slow Load Times

After going live, I noticed the blog's initial load time was approaching a full minute — clearly something was wrong. Pressing F12 to open the developer tools and checking the Network panel, I could see that every resource request was stuck on `Waiting (TTFB)`, meaning the server itself was responding slowly rather than it being a client-side rendering issue.

My debugging approach:

1. First I checked DNS: `nslookup blog.rmqg.org` — the resolution correctly pointed to Github's IP range, so DNS was fine.
2. Then I tested the server directly: `ping rmqg.github.io` — high packet loss, with latency regularly hitting two or three hundred milliseconds or timing out entirely. **Root cause identified**: Github Pages servers are located overseas, and both latency and packet loss from within China are extremely high. With every resource request suffering this delay, and the page having dozens of resources in total, the combined first-screen load time was of course absurdly slow.

The solution was to put a CDN layer inside China: user requests hit the nearest domestic CDN node, which serves from cache if available, and only fetches from the origin (Github Pages) on a cache miss. Subsequent users requesting the same resource get it straight from the node's cache without any overseas round-trip.

### Trying DogeCloud CDN (with Github Pages as Origin)

I chose `DogeCloud` because it offers a free CDN tier that's sufficient for my needs. ~~(No sponsorship involved!)~~

In the DogeCloud console, go to `CDN Acceleration → Domain Management → Add Acceleration Domain`, enter `blog.rmqg.org`, set the business type to `Web/Download`, and configure the origin settings:

- Origin protocol: `HTTPS`
- Origin address: `rmqg.github.io` (the original Github Pages domain)
- Origin host: `blog.rmqg.org`

**Pay close attention to the origin host**: it must be set to `blog.rmqg.org`, not `rmqg.github.io`. The reason is that Github Pages uses the Host header to distinguish between different users' sites. If the CDN sends a Host header of `rmqg.github.io` when fetching from Github, Github doesn't know which repository's content to return and responds with a 404. Setting it to `blog.rmqg.org` allows Github to correctly route the request to my repository.

At the same time, two things need to be done in CloudFlare's DNS:

1. Add a `_cdnauth` TXT record to complete DogeCloud's domain ownership verification (copy the value from the DogeCloud console).
2. Change the CNAME target for `blog` from `rmqg.github.io` to the DogeCloud-assigned CNAME endpoint in the format `xxxxx.doge.com`, keeping the cloud icon grey. The switch is then complete.

Next, an HTTPS certificate needs to be configured for DogeCloud. Importantly, **the Github Pages certificate cannot be used here** — it's a Let's Encrypt certificate managed by Github, and the private key is not in my possession, so there's no `privkey.pem` to upload to DogeCloud. DogeCloud offers a "Certificate Autopilot" feature where DogeCloud applies for and renews the certificate on your behalf, with no manual upload required — perfect for my situation. Just toggle it on under `HTTPS Configuration → Certificate Autopilot`.

One thing to note about Certificate Autopilot:

> The system checks the certificate expiry status of domains with Certificate Autopilot enabled every morning. Domains with no certificate configured, or whose certificate expires within 10 days, will trigger an automatic certificate renewal.

After enabling it, the certificate isn't issued immediately — it only triggers the next morning. I tried accessing `https://blog.rmqg.org` and couldn't get it to load, so I went to sleep and picked things up the next day.

Results the next day: the certificate was in place, HTTPS was working, and cached resources were noticeably faster. However, **requests that missed the cache were still slow** — CDN cache misses still had to reach back to Github Pages, and Github's own response times are inherently long. The CDN merely changed "every user is slow once" to "only the first user is slow once." For a small blog with very few visitors like mine, the cache hit rate is extremely low, so the practical improvement was quite limited.

### Switching to DogeCloud COS Object Storage as the Origin

The proper fix is to host the blog's static files directly on DogeCloud's own COS (Cloud Object Storage) and have the CDN use COS as its origin, bypassing Github Pages overseas entirely. COS servers are located in China, so origin fetch latency is on the order of tens of milliseconds, and since CDN and COS communicate over an internal network, cold-start cache performance is dramatically improved as well.

In the DogeCloud console, go to `Object Storage → Bucket List → Create Bucket`. Choose a domestic region (I'm based in Guangzhou and most of my acquaintances are in southern China, so I chose the Guangzhou node). The bucket name can be anything.

Once created, go to the domain's basic configuration in Domain Management, edit the origin type to Cloud Storage, select the bucket you just created, and confirm.

Then update the Github Actions workflow: after Hugo builds and uploads the artefact to Github Pages, add a step to sync the `public/` directory to DogeCloud COS:

```yaml
- name: 上传到多吉云 COS
  uses: zu1k/dogecloud-cos-action@v0.1
  with:
    access_key: ${{ secrets.DOGE_ACCESS_KEY }}
    secret_key: ${{ secrets.DOGE_SECRET_KEY }}
    bucket: ${{ secrets.DOGE_BUCKET }}
    region: ${{ secrets.DOGE_REGION }}
    local_path: public
    remote_path: /
    clean: true
```

`DOGE_ACCESS_KEY` and `DOGE_SECRET_KEY` are the API keys for your DogeCloud account, generated under `Account → Key Management` in the DogeCloud console. `DOGE_BUCKET` is the bucket name and `DOGE_REGION` is the region code for the bucket (check the console). All four values should be stored as Secrets in the repository under `Settings → Secrets and variables → Actions → New repository secret` (create them one by one). **Do not write them in plain text in the workflow file** — doing so would expose your keys in a public repository.

The `clean: true` parameter is important: it clears all existing files in COS before each upload, then uploads the freshly built content. This prevents stale files (such as deleted posts or images whose paths have changed) from lingering in COS and remaining accessible.

After pushing the updated workflow and waiting for Actions to complete, check the file list in DogeCloud COS — you should see all the HTML, CSS, JS, fonts, images, and other files synced over. I tested the CDN fetching from COS and everything worked correctly. First-load time dropped from tens of seconds to within two or three seconds — a very significant improvement in practice.

I also kept a backup copy on Github Pages: I removed the `Custom domain` in `Settings → Pages` and restructured the workflow to run two separate builds — one with `rmqg.github.io` as the `baseURL` and one with `blog.rmqg.org` — so that both addresses have their own independent set of working static files. If the CDN ever goes down, `rmqg.github.io` remains fully functional. To make the sequence of the two builds and deployments clearer, I refactored the workflow into three sequential jobs: `build (build for Github Pages) → deploy → upload-cos (build for COS and upload)`. The complete code is in the appendix at the end of this post.

### Also Fixed Local Proxy Bypass

During local development and testing, I had `Clash` running as a proxy and noticed that traffic to `blog.rmqg.org` was also going through the proxy node — leaving China, then coming back — which completely bypassed the domestic CDN, rendered the CDN acceleration pointless, and also interfered with my ability to judge whether the acceleration was actually working.

Clash's rule list is matched top to bottom, stopping at the first match. By inserting a few `DOMAIN-SUFFIX` direct-connection rules at the **very top** of the `rules` field in `/etc/clash/config.yaml`, traffic to those domains bypasses the proxy and connects directly:

```yaml
- DOMAIN-SUFFIX,dogecloud.com,DIRECT
- DOMAIN-SUFFIX,dogedns.com,DIRECT
- DOMAIN-SUFFIX,dogestore.com,DIRECT
- DOMAIN-SUFFIX,rmqg.org,DIRECT
```

The first three cover DogeCloud-related domains (CDN entry points, DNS, and COS storage); the last one makes my own blog domain connect directly as well. After making the change, I reloaded the Clash configuration (`sudo systemstl restart clash.server` to restart) and confirmed that `blog.rmqg.org` was now connecting directly, allowing me to properly verify the CDN configuration.

Subsequent testing revealed that the `meting-api` I had set up on `vercel` was severely slowing down page loads. In the interest of improving the blog's stability and maintainability, I switched to the API officially maintained by `injahow`: `https://injahow.github.io/meting-api/`. After making that change, the entire page loads quickly.

## Closing

I've been feeling quite lost lately — unsure of what I can do or what I should be doing. Rebuilding this blog and writing all of this down is, I suppose, a way of leaving some kind of record. A blog hosted on a VPS might vanish from the internet's memory the moment I stop maintaining it, but I believe these few dozen megabytes of data sitting on Microsoft's servers can last a little longer. Even if the project is eventually abandoned, anyone who comes along later can still find the somewhat rough-around-the-edges words of a university student at `https://github.com/rmqg/rmqg.github.io/tree/main/content/post`.

I hope the writing on this blog can offer readers a little inspiration or help. If you have any questions, please feel free to reach out — I genuinely don't mind being contacted at all.

## Appendix

Two subsequent changes were made to the `Github workflow`:

1. **`cancel-in-progress: false` → `true`**: With the original `false` setting, if you pushed multiple times in quick succession, old workflow runs would not be cancelled, causing both runs to upload an artefact named `github-pages` and triggering a `deploy-pages` Action error: "Multiple artifacts named 'github-pages' were unexpectedly found." Changing it to `true` means a new push automatically cancels the previous run, resolving the issue.

2. **Workflow refactored into three jobs**: Previously, the COS upload and the Github Pages build were in the same `build` job, making the order confusing. After refactoring, the workflow becomes three sequential jobs — `build → deploy → upload-cos` — with a much clearer logical flow. Github Pages is fully deployed before the COS version is built and uploaded.

The complete fixed code is as follows:

```yaml
name: 构建并部署 Hugo 博客

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      HUGO_VERSION: 0.160.0
    steps:
      - name: 拉取代码
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: 安装 Hugo Extended
        run: |
          curl -sLJO "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
          mkdir -p ~/.local/hugo
          tar -C ~/.local/hugo -xf "hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
          echo "$HOME/.local/hugo" >> $GITHUB_PATH

      - name: 配置 Pages
        id: pages
        uses: actions/configure-pages@v5

      - name: 构建站点（GitHub Pages）
        run: hugo --gc --minify --baseURL "https://rmqg.github.io/"

      - name: 上传构建产物到 GitHub
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: 部署到 GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4

  upload-cos:
    runs-on: ubuntu-latest
    needs: deploy
    env:
      HUGO_VERSION: 0.160.0
    steps:
      - name: 拉取代码
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: 安装 Hugo Extended
        run: |
          curl -sLJO "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
          mkdir -p ~/.local/hugo
          tar -C ~/.local/hugo -xf "hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
          echo "$HOME/.local/hugo" >> $GITHUB_PATH

      - name: 构建站点（COS 主域名）
        run: hugo --gc --minify --baseURL "https://blog.rmqg.org/"

      - name: 上传到多吉云 COS
        uses: zu1k/dogecloud-cos-action@v0.1
        with:
          access_key: ${{ secrets.DOGE_ACCESS_KEY }}
          secret_key: ${{ secrets.DOGE_SECRET_KEY }}
          bucket: ${{ secrets.DOGE_BUCKET }}
          region: ${{ secrets.DOGE_REGION }}
          local_path: public
          remote_path: /
          clean: true
```
