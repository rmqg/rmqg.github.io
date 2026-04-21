---
title: Notes on Building My Third Blog
description: Notes on Building My Third Blog

date: 2026-04-19T11:58:32+08:00
lastmod: 2026-04-19T20:52:06+08:00
---

## Prologue
Partly to have something to talk about in my cybersecurity transfer interview, I decided to revive this long-neglected blog. Since I'm a fairly lazy person, rebuilding it the same way as the previous two generations — `WordPress + MySQL + PHP` — would likely mean losing all the data the moment I got tired of maintaining the server. Deploying Blog Ver.3.0 on `GitHub Pages` neatly solves that problem: even if I go quiet for months, all posts and comments stay in the GitHub repo, safe from the cost of an expired VPS.

So I built this blog with `Hugo + GitHub Actions`. The theme is `hugo-theme-reimu`, recommended by Claude Sonnet 4.6.

{{<link title="HUGO" link="https://gohugo.io" cover="https://github.com/gohugoio/hugo/blob/master/docs/static/apple-touch-icon.png?raw=true">}}

{{<link title="hugo-theme-reimu" link="https://github.com/D-Sketon/hugo-theme-reimu" cover="https://camo.githubusercontent.com/66beeb49b45f16c66f7df739279b5da72a453aa5dd3c91730c5a39fe20eee15d/68747470733a2f2f666173746c792e6a7364656c6976722e6e65742f67682f442d536b65746f6e2f626c6f672d696d672f69636f6e2e706e67">}}

All files for this blog are in the public repository: [https://github.com/rmqg/rmqg.github.io](https://github.com/rmqg/rmqg.github.io) — feel free to use it as a reference.

## Step 1: Local Development
I noticed that `D-Sketon`, the author of `hugo-theme-reimu`, wrote in the project README:

> [!NOTE]
> Complete beginners can use `hugo-reimu-template` directly. Just clone the repo and edit the config to get a basic blog up and running!

I tried the standard flow from scratch, gave up after a few minutes, and just forked the template instead. This saved a lot of unnecessary hassle — the template offers the same customisability as the standard flow, `D-Sketon` just pre-fills a ton of default config for you.

{{<link title="hugo-reimu-template" link="https://github.com/D-Sketon/hugo-reimu-template" cover="https://camo.githubusercontent.com/66beeb49b45f16c66f7df739279b5da72a453aa5dd3c91730c5a39fe20eee15d/68747470733a2f2f666173746c792e6a7364656c6976722e6e65742f67682f442d536b65746f6e2f626c6f672d696d672f69636f6e2e706e67">}}

After forking the template and pulling it locally, follow the `hugo-theme-reimu` docs: first edit `hugo.toml` for the basic settings, then go through `config/_default/params.yml` line by line from top to bottom. ~~(Ask AI about anything you don't understand)~~

`params.yml` has a huge number of options. I went through every line and recorded all the changes below in file order. ~~(Should be all of them, I hope)~~

### Basic Info and Subtitle
First update `author`, `email`, and `description` with your own info.

The subtitle supports a typewriter animation. Configure it under `subtitle.typing`:

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

The three strings loop — typed out, then deleted. The default speed settings work great. Also updated the `text` field, which is the static fallback text when `typing.enable: false`.

Also enabled `banner_srcset` to serve different banner resolutions so mobile loads a smaller image. Changed `excerpt_link` to `继续阅读` to better match the Chinese-first nature of the blog.

### Footer and Social Links
Set `footer.since` to `2026` and `powered` to `false` to remove the "Powered by Hugo" text.

Added platform links under the `social` field — the theme renders the icons in the sidebar automatically. Filled in `email`, `github`, `bilibili`, `telegram`, `steam`, plus `qq` and `weixin` (Tencent doesn't provide APIs for these, so I saved the friend QR codes locally and referenced them directly). NetEase Cloud Music isn't in the theme's built-in icon list, so it needs extra CSS in `injector` — just put in a placeholder link for now.

### Update Time and Corner Badge
Set `show_update_time` to `true` so both the post list and post detail pages show the last modified time. Also enabled `triangle_badge` with the `github` icon pointing to my GitHub profile — a small badge appears in the top-right corner of the page.

### Fonts
Changed the body font from `Noto Serif SC` (serif, like Song typeface) to `Noto Sans SC` (sans-serif, like Hei typeface), and added `JetBrains Mono` for code (the default font wasn't great for reading on screen):

```yaml
font:
  enable: true
  article:
    - Mulish
    - Noto Sans SC
  code:
    - JetBrains Mono
```

All of these are hosted on Google Fonts — the theme loads them automatically.

### Miscellaneous Feature Toggles
Set `mermaid.zoom` to `true` so diagrams support mouse zoom. Filled in `clipboard.copyright.content` with a copyright notice that gets appended when you copy more than a certain number of characters. (Later found this only works on the code block copy button, so I ended up disabling it.)

### Comment System
Changed `comment.default` from `waline` to `giscus`, then filled in the repo config generated at [giscus.app](https://giscus.app/zh-CN):

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

`giscus` is backed by `GitHub Discussions`, so comment data lives in the repo. No worrying about a third-party service shutting down, and it fits perfectly with the low-maintenance philosophy of this version.

### Preloader, Copyright, Sponsorship, and Sharing
Changed the `preloader` loading text for each language to match the subtitle theme.

Enabled `article_copyright` to show author, title, date, last modified time, and licence. Chose `by-nc-sa`.

Filled in the Moe ICP registration number in `moe_icp.icpnumber` (just the digits).

Enabled `sponsor` with Alipay and WeChat QR codes placed in `static/sponsor/`, paths filled into the `qr` field.

Uncommented all platforms in the `share` field so a sharing bar appears at the bottom of posts.

Added a placeholder category in `home_categories` — will tidy this up properly once there are more posts.

### Code Injection (injector)
This is the messiest part. Three things injected into `injector.head_end`:
- NetEase Cloud Music icon CSS (uses `mask` + SVG to cut out the icon shape; `currentColor` inherits colour for light/dark mode)
- APlayer fixed-position style tweaks, plus a Live2d model ID init script (pre-sets the model so it doesn't randomly change on every refresh)
- `injector.body_end` got a MetingJS loop button SVG patch, fixing the missing loop icon that appeared when Meting loaded from the CDN.

~~(Most of the CSS and JS in injector was written by Claude Sonnet 4.6 — I don't understand half of it)~~

### PJAX, Live2d, and Music Player

Set `pjax.enable` to `true` so page navigation becomes partial refresh — faster transitions and the music player doesn't stop when navigating. Set `live2d_widgets.enable` to `true` so the mascot appears in the bottom-left corner.

For the music player: enabled `aplayer` with autoplay (doesn't actually trigger due to browser restrictions), shuffle mode, volume 0.3, and loop. Enabled `meting` with the NetEase playlist ID and a custom API address. (Originally set up a Vercel API with my own cookie, but later found it was the bottleneck for load time. Switched to `injahow`'s publicly maintained API.) (Note: the API URL format needs to be changed from the default — the original will throw an error):

```yaml
meting:
  enable: true
  meting_api: "https://api.injahow.cn/meting/?server=:server&type=:type&id=:id&r=:r"
  options:
    id: 17883899120
    server: netease
    type: playlist
```

Set `pangu.enable` to `true` for automatic spacing between Chinese and English characters. ~~(Because I have severe OCD)~~

### Theme Colour and Dynamic Colouring
The default `hugo-theme-reimu` is red. I prefer blue, so I replaced all `--red-*` variables under `internal_theme` with blue values — one set for light mode, one for dark. ~~(All colour codes generated by Claude Sonnet 4.6)~~ The `--red-*` names are just placeholder names in the theme; the actual colour is whatever value you set.

Later enabled `material_theme`, which automatically extracts the dominant colour from the banner image and generates a dynamic colour scheme. It pairs much better with the banner. ~~(So most of the manually tweaked colours got overridden anyway)~~

### Summary

Throughout all of the above, I ran `hugo server` locally to preview and adjust. Sometimes I also pushed to GitHub to preview the live build. Kept going until it looked right.

The configuration process isn't very intuitive without a GUI, but the logic is clear and simple enough to work through. ~~(Is this one of the advantages of projects made by Chinese developers?)~~

> [!CAUTION]
> Never modify files inside the `themes/hugo-theme-reimu` folder — it will cause Git headaches. Instead, find the file path inside `themes/hugo-theme-reimu`, create the same folder structure in your own config directory, copy the file there, and edit your copy.

## Step 2: Deploying to GitHub Pages
This step sets up `GitHub Actions` to automatically build the Hugo site and deploy it to `GitHub Pages` on every push, so you never have to do it manually.

`hugo-reimu-template` doesn't include a workflow file, so you need to create one yourself at `.github/workflows/`.

The workflow has two jobs: `build` installs Hugo, builds the site, and uploads the artifact; `deploy` depends on `build` finishing and then publishes the artifact to GitHub Pages.

A few details to note in the `build` job:

- `checkout` uses `submodules: recursive` because the theme is a git submodule — without this, the theme files won't be pulled
- `fetch-depth: 0` pulls the full git history so Hugo can correctly generate `lastmod` times for posts
- Hugo needs the `Extended` version to support Sass/SCSS — download and extract it from the GitHub Release, then add it to `PATH`

```yaml
name: Build and Deploy Hugo Blog

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
      - name: Checkout Code
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: Install Hugo Extended
        run: |
          curl -sLJO "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
          mkdir -p ~/.local/hugo
          tar -C ~/.local/hugo -xf "hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
          echo "$HOME/.local/hugo" >> $GITHUB_PATH

      - name: Configure Pages
        id: pages
        uses: actions/configure-pages@v5

      - name: Build Site
        run: hugo --gc --minify

      - name: Upload Artifact to GitHub
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
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

After writing the workflow, go to `Settings → Pages` and change `Source` to `GitHub Actions`, otherwise deployment will silently fail with no error message.

One gotcha: I originally wrote `hugo --gc --minify --baseURL "${{ steps.pages.outputs.base_url }}/"`, intending to let `configure-pages` inject the `baseURL` dynamically. It turned out to pass an `http://` address, causing all absolute links in the generated HTML to be HTTP — leading to mixed content errors everywhere in a forced-HTTPS environment. The fix was to remove the `--baseURL` flag entirely and hardcode `baseURL = 'https://blog.rmqg.org/'` in `hugo.toml`. ~~(Took ages to figure out)~~

## Step 3: Writing the About and Friends Pages
This is just writing `content/friend.md` and `content/about.md` with your own content. You can also create `content/about.en.md`, `content/about.ja.md`, `content/about.zh-tw.md`, etc. so switching the language in the top-right corner shows different language versions of the About page. (I used Claude Sonnet 4.6 to translate into the non-Chinese versions.)

## Step 4: Using a Custom Domain
Everything above runs on GitHub's domain `https://rmqg.github.io/`. This step points a custom domain at the blog and optimises connection performance.

### Binding the Custom Domain
In the GitHub repo, go to `Settings → Pages → Custom domain`, enter `blog.rmqg.org`, and save. GitHub automatically creates a `CNAME` file at the root of the repo (containing just `blog.rmqg.org`) and immediately triggers a build to commit it. Don't push anything else until that build finishes.

The domain is hosted on `CloudFlare`. Add a `CNAME` record in the DNS panel: name `blog`, target `rmqg.github.io`, cloud icon kept **grey** (Proxied off — DNS only). Once DNS propagates (usually a few minutes to half an hour), `blog.rmqg.org` is accessible.

> [!TIP]
> Once a custom domain is bound, visiting `rmqg.github.io` is automatically 302-redirected to `blog.rmqg.org` by GitHub. This is built into GitHub Pages — no redirect rules needed.

Back in GitHub Pages settings, wait for GitHub to verify the DNS, then tick `Enforce HTTPS`. GitHub auto-provisions and renews a Let's Encrypt certificate. Note that this certificate is GitHub-managed — the private key is not accessible, which matters when connecting a CDN later.

> [!NOTE]
> If `Enforce HTTPS` is greyed out right after binding the domain, wait a few minutes for GitHub to finish provisioning the certificate.

### Tried CloudFlare Orange Cloud First
My initial idea was to turn the CloudFlare cloud orange and let CF's CDN proxy all traffic. Testing showed this barely helped for mainland China access — the free tier routes through CF's international network, not actual mainland China nodes. CF's China Network (which does use mainland nodes) requires ICP registration and a separate application. Not available for a personal blog without a filing.

So CloudFlare stays grey (DNS only), and the acceleration job is handed off to a Chinese CDN.

### Discovered Very Slow Loading
After going live, first load times were close to a minute — obviously wrong. Opening DevTools and looking at the Network tab, every resource request was stuck on `Waiting (TTFB)`, meaning the server itself was slow.

Diagnosis:

1. DNS check: `nslookup blog.rmqg.org` resolved correctly to GitHub's IP range — DNS is fine
2. Direct server test: `ping rmqg.github.io` — high packet loss, latency often 200–300ms or timing out. **Root cause found**: GitHub Pages servers are overseas; every single resource request on a page with dozens of assets adds up to an absurd first-load time

The fix is to put a domestic CDN in front — requests hit the nearest Chinese CDN node, cached resources are returned instantly, only cache misses go all the way back to the origin.

### Tried DogeCloud CDN (Origin: GitHub Pages)
`DogeCloud` has a generous free CDN tier, so I went with it. ~~(I'm not sponsored)~~

In the DogeCloud console under `CDN → Domain Management → Add Domain`, enter `blog.rmqg.org`, type `Web/Download`, and configure the origin:

- Origin protocol: `HTTPS`
- Origin address: `rmqg.github.io`
- Origin host: `blog.rmqg.org`

**The origin host is important**: it must be `blog.rmqg.org`, not `rmqg.github.io`. GitHub Pages uses the Host header to route requests to the correct repo — if the CDN sends `rmqg.github.io` as the Host, GitHub doesn't know which repo to serve and returns 404. Using `blog.rmqg.org` routes it correctly.

Then in CloudFlare DNS, two things:

1. Add a `_cdnauth` TXT record for DogeCloud domain ownership verification (copy the value from the DogeCloud console)
2. Change the `blog` CNAME target from `rmqg.github.io` to the `xxxxx.doge.com` CNAME endpoint assigned by DogeCloud — keep the cloud grey

For the HTTPS certificate: **you cannot use the GitHub Pages certificate** — it's a GitHub-managed Let's Encrypt cert and the private key is inaccessible. DogeCloud has a "Worry-Free Cert" feature that auto-provisions and renews the certificate without you needing to upload anything. Enable it under `HTTPS Config → Worry-Free Cert`.

One catch: the system only runs its daily check **in the morning**. After enabling, it won't issue immediately — you have to wait until the next morning. I couldn't access `https://blog.rmqg.org` and couldn't figure out why, spent some time checking the config, then just went to sleep. Woke up the next morning and it worked. ~~(Wasted a whole afternoon)~~

Next-day test: HTTPS worked, cached resources loaded quickly — but **cache misses were still slow**. The CDN still has to hit GitHub Pages on a cold cache, and GitHub's response time is slow regardless. The CDN just turns "everyone waits once" into "only the first person waits once" — with virtually no traffic on a personal blog, the cache hit rate is negligible.

### Switched to DogeCloud COS as Origin
The real fix is to host the static files on DogeCloud's own COS (object storage) and have the CDN source from COS — completely bypassing overseas GitHub Pages. COS is domestic, round-trip latency is tens of milliseconds, and CDN-to-COS is internal network so cold starts are fast too.

In the DogeCloud console, `Object Storage → Bucket List → New Bucket`. Pick a domestic region (I chose Guangzhou since I'm based there), name doesn't matter.

After creating the bucket, go to the CDN domain's `Basic Config → Origin Info`, change the origin type to Cloud Storage, select the bucket, and save.

Then modify the GitHub Actions workflow to upload `public/` to DogeCloud COS after the Hugo build:

```yaml
- name: Upload to DogeCloud COS
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

`DOGE_ACCESS_KEY` and `DOGE_SECRET_KEY` are the DogeCloud API keys from `Account → Key Management`. `DOGE_BUCKET` is the bucket name, `DOGE_REGION` is the region code (check in the console). Add all four as Secrets under `Settings → Secrets and variables → Actions → New repository secret`. **Do not hardcode them in the workflow file** — the repo is public.

`clean: true` is important: it wipes the bucket before uploading, preventing stale files (deleted posts, renamed images) from lingering.

After pushing, verify the files in the DogeCloud COS file list — all HTML, CSS, JS, fonts, and images should be there. CDN sourcing from COS works perfectly. First load time dropped from nearly a minute to 2–3 seconds.

GitHub Pages also keeps a backup copy: remove the `Custom domain` in `Settings → Pages`, then build the site twice in the workflow — once with `rmqg.github.io` as `baseURL` and once with `blog.rmqg.org` — so both addresses have fully self-contained static files. If the CDN goes down, `rmqg.github.io` still works independently. To keep the build and deploy sequence clear, the workflow was refactored into three serial jobs: `build (GitHub Pages version) → deploy → upload-cos (COS version + upload)`. See the appendix at the end for the complete code.

### Fixed Proxy Bypass on Local Machine
With `Clash` running, traffic to `blog.rmqg.org` was going through the proxy — out of the country and back in, completely bypassing the domestic CDN. Also made it impossible to accurately test the CDN's actual effect.

Clash matches rules top-down and stops at the first match. Just insert a few `DOMAIN-SUFFIX` DIRECT rules at the **very top** of the `rules` field in `/etc/clash/config.yaml`:

```yaml
- DOMAIN-SUFFIX,dogecloud.com,DIRECT
- DOMAIN-SUFFIX,dogedns.com,DIRECT
- DOMAIN-SUFFIX,dogestore.com,DIRECT
- DOMAIN-SUFFIX,rmqg.org,DIRECT
```

The first three cover DogeCloud domains (CDN endpoint, DNS, COS). The last one makes my own blog go direct. Reload Clash config and traffic goes direct — finally able to see the actual CDN performance.

After that, testing revealed that the self-hosted `meting-api` on Vercel was significantly slowing down page loads. In the spirit of keeping the blog stable and low-maintenance, I switched to `injahow`'s publicly maintained API: `https://injahow.github.io/meting-api/`. After that change, the whole page loads quickly.

## Closing
I've been feeling pretty lost lately — not sure what I can or should be doing. Rebuilding this blog and writing all this down is partly just to leave some kind of record. A blog on a VPS might vanish when I stop paying the bills, but I'd like to think these few dozen megabytes sitting on Microsoft's servers will last a bit longer. Even if the project goes unmaintained, someone in the future can still find a university student's somewhat naive words at `https://github.com/rmqg/rmqg.github.io/tree/main/content/post`.

I hope something in this blog is useful or interesting to whoever reads it. Feel free to reach out with any questions — I genuinely don't mind being contacted.

## Appendix
Two fixes were made to the GitHub workflow after the initial setup:

1. **`cancel-in-progress: false` → `true`**: With the original `false`, rapid consecutive pushes left old workflow runs alive. Both runs would upload an artifact named `github-pages`, causing `deploy-pages` to error with "Multiple artifacts named 'github-pages' were unexpectedly found". Setting it to `true` cancels old runs automatically.

2. **Refactored into three jobs**: Originally the COS upload and GitHub Pages build were in the same `build` job in a confusing order. Refactored to `build → deploy → upload-cos` — cleaner logic, and GitHub Pages deploys before the COS version is built.

Final complete workflow:

```yaml
name: Build and Deploy Hugo Blog

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
      - name: Checkout Code
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: Install Hugo Extended
        run: |
          curl -sLJO "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
          mkdir -p ~/.local/hugo
          tar -C ~/.local/hugo -xf "hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
          echo "$HOME/.local/hugo" >> $GITHUB_PATH

      - name: Configure Pages
        id: pages
        uses: actions/configure-pages@v5

      - name: Build Site (GitHub Pages)
        run: hugo --gc --minify --baseURL "https://rmqg.github.io/"

      - name: Upload Artifact to GitHub
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
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4

  upload-cos:
    runs-on: ubuntu-latest
    needs: deploy
    env:
      HUGO_VERSION: 0.160.0
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: Install Hugo Extended
        run: |
          curl -sLJO "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
          mkdir -p ~/.local/hugo
          tar -C ~/.local/hugo -xf "hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
          echo "$HOME/.local/hugo" >> $GITHUB_PATH

      - name: Build Site (COS Main Domain)
        run: hugo --gc --minify --baseURL "https://blog.rmqg.org/"

      - name: Upload to DogeCloud COS
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

---

*Translation provided by `Claude Sonnet 4.6`*
