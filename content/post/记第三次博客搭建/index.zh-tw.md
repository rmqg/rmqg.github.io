---
title: 記第三次部落格搭建
description: 詳細記錄第三代部落格從本地除錯、Hugo主題配置、GitHub Actions自動部署，到接入自訂網域、多吉雲CDN加速與COS物件儲存的完整搭建過程，並附完整工作流程程式碼。

date: 2026-04-19T11:58:32+08:00
lastmod: 2026-10-23T21:51:19+08:00

categories:
  - 技術
  - 折騰
tags:
  - 部落格
  - Hugo
  - GitHub Actions
  - CDN
---

## 序

大概是為了在資安轉系面試的時候有點東西可以用來吹噓，所以決定復活已經好久沒有認真維護的 Blog，又因為作者比較懶散，若還是和前兩代 Blog 一樣使用 `WordPress+MySql+PHP` 搭建，很可能因為疏於維護伺服器而遺失資料。將 Blog Very.3.0 部署在 `Github Pages` 上則可以很好地應對這個問題，即使怠於維護，所有的文章、留言等都會保留在 Github 專案裡，而不用擔心伺服器到期造成的損失。

因此，我使用了 `Hugo+Github Actions` 的組合搭建了這個 Blog，所選用主題為 Claude Sonnet 4.6 推薦的二次元主題 `hugo-theme-reimu`。

{{<link title="HUGO" link="https://gohugo.io" cover="https://github.com/gohugoio/hugo/blob/master/docs/static/apple-touch-icon.png?raw=true">}}

{{<link title="hugo-theme-reimu" link="https://github.com/D-Sketon/hugo-theme-reimu" cover="https://camo.githubusercontent.com/66beeb49b45f16c66f7df739279b5da72a453aa5dd3c91730c5a39fe20eee15d/68747470733a2f2f666173746c792e6a7364656c6976722e6e65742f67682f442d536b65746f6e2f626c6f672d696d672f69636f6e2e706e67">}}

本 Blog 的所有檔案儲存於 Republic Repository：[https://github.com/rmqg/rmqg.github.io](https://github.com/rmqg/rmqg.github.io)，讀者可自行參考對照。

## Step 1：本地除錯

注意到，`hugo-theme-reimu` 的作者 `D-Sketon` 大大在專案的 md 中表示：

> [!NOTE]
> 純新手可以直接使用 `hugo-reimu-template`。只需 複製倉庫-修改設定 即可獲得一個基本的部落格！

作者嘗試按照標準流程一步一步手刻 Blog，稍作嘗試便放棄了，fork 了整個模板專案，然後以此為基礎開發，省去了許多不必要的麻煩（模板專案和標準流程的可定義性是一樣的，只是 `D-Sketon` 大大幫你完成了許多預設設定）。

{{<link title="hugo-reimu-template" link="https://github.com/D-Sketon/hugo-reimu-template" cover="https://camo.githubusercontent.com/66beeb49b45f16c66f7df739279b5da72a453aa5dd3c91730c5a39fe20eee15d/68747470733a2f2f666173746c792e6a7364656c6976722e6e65742f67682f442d536b65746f6e2f626c6f672d696d672f69636f6e2e706e67">}}

fork template 庫並 pull 到開發終端後，可以按照 `hugo-theme-reimu` 專案的教學，先修改 `hugo.toml` 檔案完成基本設定，再從上往下逐行修改 `config/_default/params.yml` 的設定，對原有的 template 做自己的客製化調整。~~（有看不懂的設定語句就問 AI）~~

`params.yml` 改動量相當大，作者從上到下逐行啃完，以下按檔案順序記錄所有改動~~（應該是所有的改動沒有遺漏吧）~~。

### 基本資訊與副標題

先修改 `author`、`email` 和 `description` 三項，填入自己的資訊。

副標題的 `hugo-theme-reimu` 支援打字機動畫效果，可在 `subtitle.typing` 下設定語句：

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

三條句子會循環打出再刪除，預設的速度等參數效果就很不錯。`text` 欄位是 `typing.enable: false` 時的靜態回退文字，也一併修改。

順帶開啟了 `banner_srcset`，設定不同解析度的 Banner 圖片，行動裝置端載入較小的版本。`excerpt_link` 也改成了 `繼續閱讀`，更符合部落格以中文為主的思想。

### 頁尾與社群連結

`footer.since` 根據實際情況改為 `2026`，`powered` 設為 `false` 去掉「Powered by Hugo」字樣。

`social` 欄位下填入各平台連結，主題會在側邊欄自動渲染對應圖示，填了 `email`、`github`、`bilibili`、`telegram`、`steam`，以及 `qq` 和 `weixin`（這兩項因為騰訊這個傻瓜不提供介面，只能將加好友 QR Code 儲存在本地並呼叫）。`網易雲音樂` 不在主題內建圖示清單裡，需要後面在 `injector` 裡單獨處理（這部分 CSS 的編輯由……），這裡先填寫連結佔位。

### 顯示更新時間與角標

`show_update_time` 設為 `true`，文章列表和詳情頁會額外顯示最後修改時間。`triangle_badge` 也開啟，圖示選 `github`，連結填自己的主頁，頁面右上角會多一個角標指向我的 Github 首頁。

### 字型

正文字型從 `Noto Serif SC`（襯線，類似宋體）改為 `Noto Sans SC`（無襯線，類似黑體），程式碼字型加入了 `JetBrains Mono`（因為作者覺得原來的字型不適合在網頁上閱讀）：

```yaml
font:
  enable: true
  article:
    - Mulish
    - Noto Sans SC
  code:
    - JetBrains Mono
```

以上字型都由 Google Fonts 託管，主題會自動載入，無需額外設定。

### 雜項功能開關

`mermaid.zoom` 設為 `true`，流程圖支援滑鼠縮放；`clipboard.copyright.content` 填入版權聲明文字，複製超過一定字元數時自動附加（最後發現這項功能只在程式碼區塊的複製按鈕生效，在後續修改中被我停用了此項功能）。

### 留言系統

`comment.default` 從 `waline` 改為 `giscus`，再在 `giscus` 欄位下填入從 [giscus.app](https://giscus.app/zh-CN) 產生的倉庫設定：

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

`giscus` 基於 `GitHub Discussions` 實現，留言資料儲存在倉庫裡，不用擔心第三方服務跑路，也符合了作者這個版本以省心免維護為宗旨的目標。

### 預載入、版權聲明、打賞與分享

`preloader` 各語言的載入文字改成了與副標題呼應的句子。

`article_copyright` 開啟，設定顯示作者、標題、日期、更新時間和授權條款，授權條款類型選 `by-nc-sa`。

`moe_icp.icpnumber` 填入萌國備案號（只填數字部分就行了）。

`sponsor` 開啟，支付寶和微信收款碼放在 `static/sponsor/` 目錄，`qr` 欄位填入路徑。

`share` 欄位把常用的幾個平台全部取消註解，文章底部會出現分享列。

`home_categories` 裡順手填了一個測試分類佔位，後續文章多了再整理。

### 程式碼注入（injector）

這是改動最雜的一塊。`injector.head_end` 裡注入了三段內容：
- 網易雲圖示 CSS（用 `mask`+SVG 裁出圖示形狀，`currentColor` 繼承顏色實現亮暗模式適配）
- APlayer 固定定位的樣式微調、以及一段 Live2d 模型 ID 初始化腳本（預設模型避免每次重新整理隨機更換）
- `injector.body_end` 裡注入了 MetingJS 循環按鈕 SVG 的修復 patch，解決雲端 Meting 載入時循環圖示遺失的問題。

~~（injector 裡的 CSS 和 JS 基本都是 Claude Sonnet 4.6 修改的，作者看不懂）~~

### PJAX、Live2d 與音樂播放器

`pjax.enable` 設為 `true`，頁面跳轉變為局部重新整理，導覽更快，音樂播放器也不會因為跳頁而中斷。`live2d_widgets.enable` 設為 `true`，看板娘出現在頁面左下角。

音樂播放器部分開啟 `aplayer` 並設定自動播放（雖然好像因為瀏覽器限制實際上觸發不了）、隨機順序、音量 0.3、列表循環等選項，再開啟 `meting` 並填入網易雲歌單 ID 和自訂 API 位址（本來在 vercel 設定了一個 api，使用了自己的 cookie，在後續優化連線延遲的時候發現此處成為瓶頸，最終使用了 `injahow` 自己維護的 api 介面）（此處呼叫 api 的語句應進行修改，原來的會報一個錯誤）：

```yaml
meting:
  enable: true
  meting_api: "https://api.injahow.cn/meting/?server=:server&type=:type&id=:id&r=:r"
  options:
    id: 17883899120
    server: netease
    type: playlist
```

`pangu.enable` 設為 `true`，自動在中英文之間插入空格。~~（因為作者是強迫症晚期）~~

### 主題色與動態配色

原版 `hugo-theme-reimu` 是紅色系，作者偏好藍色，把 `internal_theme` 下所有 `--red-*` 變數替換為藍色值，亮色和暗色模式各一套。~~（所有顏色編碼由 Claude Sonnet 4.6 生成）~~ 變數名叫 `--red-*` 只是主題的佔位符命名，實際顏色由填寫的值表示。

後來開啟了 `material_theme`，根據 Banner 圖片自動提取主色調生成動態配色，和 Banner 搭配起來更協調，~~（因此手動改的顏色基本都被蓋掉了）~~。

### 小結

進行以上操作時本地執行 `hugo server` 反覆預覽調整，有時也會 push 到 Github 預覽，直到滿意為止。

整體的設定步驟由於沒有 GUI 輔助不甚直觀，但邏輯簡明易懂，設定起來還算簡單~~（這就是國人開發的專案的優點之一嗎）~~。

> [!CAUTION]
> 修改任何檔案請不要在 `themes/hugo-theme-reimu` 資料夾中修改，否則會出現 `Git` 使用上的麻煩，應當參照檔案在 `themes/hugo-theme-reimu` 中的位置，在你自己的設定資料夾中新建資料夾，將需要修改的設定複製進去，然後再進行修改。

## Step 2：上傳到 Github Page

這一步是讓 `Github Actions` 在每次 push 程式碼後自動建置 Hugo 站台並部署到 `Github Pages`，省去手動操作。

`hugo-reimu-template` 裡沒有內建工作流程檔案，需要自己在 `.github/workflows/` 目錄下新建一個 `yaml` 檔案。

整個工作流程分兩個 job：`build` 負責安裝 Hugo、建置站台並上傳產物，`deploy` 依賴 `build` 完成後將產物正式發布到 `Github Pages`。

`build` job 裡有幾個細節需注意：

- `checkout` 時加了 `submodules: recursive`，因為主題是以子模組形式引入的，不加這個參數主題檔案會拉不到
- `fetch-depth: 0` 讓 git 拉取完整歷史，這樣 Hugo 才能正確生成文章的 `lastmod` 時間
- Hugo 需要安裝 `Extended` 版本才能支援 Sass/SCSS，從 GitHub Release 直接下載解壓後加入 `PATH` 即可

```yaml
name: 構建並部署 Hugo 博客

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
      - name: 拉取代碼
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: 安裝 Hugo Extended
        run: |
          curl -sLJO "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
          mkdir -p ~/.local/hugo
          tar -C ~/.local/hugo -xf "hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
          echo "$HOME/.local/hugo" >> $GITHUB_PATH

      - name: 配置 Pages
        id: pages
        uses: actions/configure-pages@v5

      - name: 構建站點
        run: hugo --gc --minify

      - name: 上傳構建產物到github
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

工作流程寫完後還需要去倉庫 `Settings → Pages` 把 `Source` 改為 `Github Actions`，否則部署會靜默失敗，什麼提示都沒有。

期間踩了一個坑：最初建置指令寫的是 `hugo --gc --minify --baseURL "${{ steps.pages.outputs.base_url }}/"`，意圖是讓 `configure-pages` 這個 Action 動態傳入 `baseURL`，結果它傳進來的是 `http://` 開頭的位址，導致生成出來的 HTML 裡所有絕對連結都是 HTTP，在強制 HTTPS 的環境下全部 mixed content 報錯。最後的修法是把 `--baseURL` 參數從建置指令裡刪掉，直接在 `hugo.toml` 裡硬編碼 `baseURL = 'https://blog.rmqg.org/'`，問題解決。~~（找了好半天）~~

## Step 3：編寫「關於」和「友站連結」

這部分操作就是編寫 `content/friend.md` 和 `content/about.md` 兩個檔案，在裡面填入自己的文字，同時可以另外編寫 `content/about.en.md`、`content/about.ja.md`、`content/about.zh-tw.md` 等檔案，這樣在頁面右上角切換語言的時候能看到不同語言版本的 `關於` 等（作者用 Claude Sonnet 4.6 翻譯出除中文外的語言版本）。

## Step 4：接入自己的網域

以上的操作都是在 Github 的網域 `https://rmqg.github.io/` 上完成，後續的操作即使用自己的網域指向 Blog 並做連線效能優化。

### 綁定自訂網域

首先在 Github 倉庫 `Settings → Pages → Custom domain` 填入 `blog.rmqg.org` 並儲存，Github 會自動在倉庫根目錄生成一個 `CNAME` 檔案（內容就是一行 `blog.rmqg.org`），並立刻觸發一次建置部署把這個檔案打進去（最終測試的時候發現訪問 `rmqg.github.io` 實際上會重新導向到 `rmqg.org`，疑似因為瀏覽器快取了棄用的 DNS 解析，換用無痕模式則無此問題）。

網域託管在 `CloudFlare`，在 DNS 面板新增一條 `CNAME` 記錄：名稱填 `blog`，目標填 `rmqg.github.io`，右側的雲朵圖示保持**灰色**（即 Proxied 關閉，僅 DNS 解析模式），儲存後等待 DNS 生效——生效時間一般幾分鐘到半小時不等，之後用 `blog.rmqg.org` 就能訪問了。

> [!TIP]
> 綁定自訂網域之後，訪問 `rmqg.github.io` 會被 Github 自動 302 重新導向到 `blog.rmqg.org`，這是 Github Pages 的內建邏輯，與 CloudFlare 無關，不用單獨設定任何跳轉規則。

回到 Github Pages 設定頁，等待 Github 識別到 DNS 正常後，勾選 `Enforce HTTPS`，Github 會自動透過 Let's Encrypt 簽發憑證並在到期前自動續期。但是 Github 給的這張憑證是 Github 代管的，無法匯出私鑰，後面接 CDN 時要注意這一點。

> [!NOTE]
> 如果剛綁完網域發現 `Enforce HTTPS` 選項是灰的，等幾分鐘讓 Github 簽完憑證就能勾了。

### 曾經考慮過用 CloudFlare 橙雲做加速

作者最初設想是直接開啟 CloudFlare 橙雲，讓 CF 的 CDN 代理所有流量。測試後發現這條路經由國內訪問很慢，初次訪問需要幾十秒才能部分載入頁面（部分 CSS 無法渲染），遂尋找其他路徑。

所以 CloudFlare 這裡始終保持灰雲（僅 DNS），把加速任務交給後面的國內 CDN。

### 發現載入很慢

上線之後發現 Blog 的首次載入時間快奔一分鐘去了，明顯不正常，按 F12 打開開發者工具，Network 面板一看，資源請求全卡在 `Waiting (TTFB)` 上，說明伺服端回應本身就慢，不是客戶端渲染的問題。

排查思路：

1. 先排查 DNS：`nslookup blog.rmqg.org`，解析結果正常指向 Github 的 IP 段，DNS 沒問題
2. 再直接測伺服端：`ping rmqg.github.io`，丟包率高，延遲動輒兩三百 ms 甚至逾時——**根本原因找到了**：Github Pages 的伺服器在境外，國內訪問延遲與丟包率極高，每個資源檔案的請求都有這個延遲，頁面一共幾十個資源，全加起來首屏載入當然慢到離譜

解法方向是在境內架一層 CDN，使用者的請求打到離他最近的國內 CDN 節點，節點有快取就直接回傳，快取沒命中才向源站（Github Pages）回源拉一次，後續其他使用者訪問同一資源就直接從節點取快取，不再繞境外。

### 嘗試多吉雲 CDN（回源 Github Pages）

`多吉雲` 由於有夠用的免費 CDN 套餐，故選擇之`（作者沒有恰米！）`

在多吉雲控制台 `CDN加速 → 域名管理 → 添加加速域名`，填入 `blog.rmqg.org`，業務類型選 `網頁/下載`，然後設定回源資訊：

- 回源協議：`HTTPS`
- 回源地址：`rmqg.github.io`（Github Pages 的原始網域）
- 回源 host：`blog.rmqg.org`

**回源 host 應當注意**：必須填 `blog.rmqg.org`，不能填 `rmqg.github.io`。原因是 Github Pages 用 Host 標頭來區分不同使用者的站台，CDN 向 Github 回源時如果 Host 標頭是 `rmqg.github.io`，Github 不知道要回傳哪個倉庫的內容，直接 404。填成 `blog.rmqg.org` 之後 Github 才能正確路由到作者的倉庫。

同時，在 CloudFlare 的 DNS 裡完成兩件事：

1. 加一條 `_cdnauth` 的 TXT 記錄完成多吉雲的網域歸屬驗證（值從多吉雲控制台複製）
2. 把 `blog` 的 CNAME 目標從 `rmqg.github.io` 改成多吉雲分配的 `xxxxx.doge.com` 格式 CNAME 接入點，灰雲保持不動，切換完成

然後要給多吉雲設定 HTTPS 憑證。需要注意的是，這裡**不能用 Github Pages 的憑證**，因為那張憑證是 Github 代管的 Let's Encrypt 憑證，私鑰不在作者手中，根本沒有可匯出的 `privkey.pem` 可以上傳給多吉雲。多吉雲提供了一個 `證書無憂` 功能，由多吉雲自己代申請並續期憑證，不需要手動上傳，對作者這種情況正合適，在 `HTTPS配置 → 證書無憂` 裡打開開關就行。

不過證書無憂需要注意的是：

> 系統將於每天上午檢查開啟了證書無憂服務的域名證書到期情況，未配置證書的，或在證書到期前 10 天內的域名，將觸發證書自動更新。

開啟之後不會立刻簽發，要等到第二天早上才觸發申請。作者訪問 `https://blog.rmqg.org` 一直無法正常訪問，遂去睡覺，第二天起來繼續工作。

第二天的測試效果：憑證有了，HTTPS 能訪問了，有快取的資源確實快了，但**快取沒有命中的時候依然很慢**——CDN 回源要打到 Github Pages 伺服器，Github 那邊的回應時間本身就長，CDN 只是把「每個使用者都慢一次」變成了「只有第一個使用者慢一次」，對於作者這種訪客極少的小 Blog 來說快取命中率極低，實際改善效果相當有限。

### 改用多吉雲 COS 物件儲存為源

治本的辦法是把 Blog 的靜態檔案直接託管到多吉雲自己的 COS（物件儲存）上，CDN 以 COS 為回源，徹底繞開境外的 Github Pages。COS 伺服器在國內，回源延遲幾十毫秒量級，而且是內網互通，CDN 的快取冷啟動速度也大幅提升。

在多吉雲控制台 `對象存儲 → 存儲桶列表 → 新建存儲桶`，地區選一個國內節點（作者因為人在廣州，熟人也以南方居多，選擇了廣州節點），名稱隨意。

建立完成後，在網域管理的基本設定-源站資訊中編輯源站類型為雲端儲存，選擇剛剛建立的儲存空間，確認修改。

然後修改 Github Actions 工作流程，在 Hugo 建置完、上傳產物到 Github Pages 之後，加一步把 `public/` 目錄同步上傳到多吉雲 COS：

```yaml
- name: 上傳到多吉雲 COS
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

`DOGE_ACCESS_KEY` 和 `DOGE_SECRET_KEY` 是多吉雲帳號的 API 金鑰，在多吉雲控制台 `帳號 → 密鑰管理` 裡生成。`DOGE_BUCKET` 是儲存桶名稱，`DOGE_REGION` 是儲存桶所在地區的代碼（控制台裡查），這四個值都作為 Secret 設定在倉庫 `Settings → Secrets and variables → Actions → New repository secret` 裡（逐一建立），**不要明文寫在工作流程檔案裡**，否則金鑰會隨公開倉庫一起暴露出去。

`clean: true` 這個參數很重要：每次上傳前會先清空 COS 裡的所有舊檔案，再上傳新建置的內容。這樣可以避免歷史遺留檔案（比如刪掉的文章、改過路徑的圖片）繼續留在 COS 裡被訪問到。

工作流程改完後 push，Actions 跑完後去多吉雲 COS 的檔案列表裡確認，應該能看到所有的 HTML、CSS、JS、字型、圖片等檔案都同步過來了。CDN 從 COS 回源測試一切正常，首次載入時間從原來的幾十秒縮短到兩三秒以內，實測效果非常顯著。

Github Pages 那邊也保留著一份備份：在 `Settings → Pages` 取消 `Custom domain`，再把工作流程改成建置兩次，分別以 `rmqg.github.io` 和 `blog.rmqg.org` 為 `baseURL`，這樣兩個位址各自擁有獨立可用的靜態檔案，CDN 掛了 `rmqg.github.io` 也能正常瀏覽。最終為了讓兩次建置和部署順序更清晰，把工作流程重構為三個串行的 job：`build（建置 Github Pages 版）→ deploy（部署）→ upload-cos（建置 COS 版並上傳）`，完整程式碼見文末附錄。

### 順手處理了一下本機代理繞行問題

本地開發除錯時掛著 `Clash` 代理，卻發現訪問 `blog.rmqg.org` 的流量也走了代理節點——先出國，再回來，等於完全繞過了國內的 CDN，CDN 加速白配了，而且還干擾了作者判斷加速效果。

Clash 的規則列表是從上往下匹配的，匹配到第一條就停止，不再檢查後續規則。只需要在 `/etc/clash/config.yaml` 的 `rules` 欄位**最前面**插入幾條 `DOMAIN-SUFFIX` 直連規則，就能讓這些網域的流量繞開代理直連：

```yaml
- DOMAIN-SUFFIX,dogecloud.com,DIRECT
- DOMAIN-SUFFIX,dogedns.com,DIRECT
- DOMAIN-SUFFIX,dogestore.com,DIRECT
- DOMAIN-SUFFIX,rmqg.org,DIRECT
```

前三條是多吉雲相關網域（CDN 接入點、DNS、COS 儲存），最後一條讓作者自己的 Blog 網域也走直連。改完之後重載 Clash 設定（`sudo systemstl restart clash.server` 重啟），再訪問 `blog.rmqg.org` 就走直連了，可驗證 CDN 設定效果。

後續測試發現作者使用 `vercel` 搭建的 `meting-api` 嚴重拖慢了網頁載入，本著提升 Blog 穩定性和可維護性的原則，我使用了 `injahow` 官方維護的 Api：`https://injahow.github.io/meting-api/`。修改完成後整個網頁可以快速地訪問。

## 終

作者最近也非常迷茫，不知道自己可以做些什麼，應當做些什麼，重新搭建 Blog 寫下這些文字也是想留下一點記錄吧。建在 VPS 上的 Blog 可能隨著作者停止維護而消失在網際網路的記憶中，但我相信，保存在微軟伺服器上的這幾十 MB 資料，可以保留得更久遠一點。即便專案停止維護了，後來者依舊可以在 `https://github.com/rmqg/rmqg.github.io/tree/main/content/post` 中找到一名大學生寫下的一些青澀的 token 吧。

希望這個 Blog 的文字可以對讀者有一點啟發、幫助。有任何疑問請聯絡作者，作者完全不討厭被人聯絡。

## 附

後續對 `Github workflow` 進行了兩處修改：

1. **`cancel-in-progress: false` → `true`**：原來設為 `false`，如果短時間內連續 push，舊的工作流程不會被取消，兩次執行都會上傳名為 `github-pages` 的 artifact，導致 `deploy-pages` Action 報錯「Multiple artifacts named 'github-pages' were unexpectedly found」。改為 `true` 後新的 push 會自動取消舊的執行，問題解決。

2. **工作流程重構為三個 job**：原來 COS 上傳和 Github Pages 建置在同一個 `build` job 裡，順序混亂。重構後變成 `build → deploy → upload-cos` 三個串行 job，邏輯更清晰，Github Pages 先部署完成後再建置 COS 版本上傳。

修復後的完整程式碼如下：

```yaml
name: 構建並部署 Hugo 博客

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
      - name: 拉取代碼
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: 安裝 Hugo Extended
        run: |
          curl -sLJO "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
          mkdir -p ~/.local/hugo
          tar -C ~/.local/hugo -xf "hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
          echo "$HOME/.local/hugo" >> $GITHUB_PATH

      - name: 配置 Pages
        id: pages
        uses: actions/configure-pages@v5

      - name: 構建站點（GitHub Pages）
        run: hugo --gc --minify --baseURL "https://rmqg.github.io/"

      - name: 上傳構建產物到 GitHub
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
      - name: 拉取代碼
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: 安裝 Hugo Extended
        run: |
          curl -sLJO "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
          mkdir -p ~/.local/hugo
          tar -C ~/.local/hugo -xf "hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
          echo "$HOME/.local/hugo" >> $GITHUB_PATH

      - name: 構建站點（COS 主域名）
        run: hugo --gc --minify --baseURL "https://blog.rmqg.org/"

      - name: 上傳到多吉雲 COS
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
