---
title: 第三回目のブログ構築記録
description: 第三世代ブログの構築過程を詳細に記録。ローカルデバッグ・Hugoテーマの設定・GitHub Actionsによる自動デプロイから、カスタムドメインの導入・多吉云CDNによる高速化・COSオブジェクトストレージの連携まで、完全なワークフローコードを添えて網羅している。

date: 2026-04-19T11:58:32+08:00
lastmod: 2026-10-23T21:51:19+08:00

categories:
  - 技術
  - 試行錯誤
tags:
  - ブログ
  - Hugo
  - GitHub Actions
  - CDN
---

## 序文

ネットワークセキュリティへの転専攻面接で話のネタになるものが欲しかったため、長らく放置していたBlogを復活させることにした。筆者はかなりズボラな性格なので、前の二世代のBlogと同様に`WordPress+MySql+PHP`で構築すると、サーバーのメンテナンスを怠って再びデータを失いかねない。Blog Very.3.0を`Github Pages`にデプロイすれば、この問題にうまく対処できる。更新をサボっても、すべての記事やコメントはGithubのリポジトリに残り続け、サーバーの期限切れによる損失を心配する必要がない。

そこで、`Hugo+Github Actions`の組み合わせでこのBlogを構築した。採用したテーマは、Claude Sonnet 4.6が推薦した二次元テーマ`hugo-theme-reimu`だ。

{{<link title="HUGO" link="https://gohugo.io" cover="https://github.com/gohugoio/hugo/blob/master/docs/static/apple-touch-icon.png?raw=true">}}

{{<link title="hugo-theme-reimu" link="https://github.com/D-Sketon/hugo-theme-reimu" cover="https://camo.githubusercontent.com/66beeb49b45f16c66f7df739279b5da72a453aa5dd3c91730c5a39fe20eee15d/68747470733a2f2f666173746c792e6a7364656c6976722e6e65742f67682f442d536b65746f6e2f626c6f672d696d672f69636f6e2e706e67">}}

このBlogのすべてのファイルはRepublic Repositoryに保存されている：[https://github.com/rmqg/rmqg.github.io](https://github.com/rmqg/rmqg.github.io)。読者は自由に参照してほしい。

## Step 1：ローカルデバッグ

`hugo-theme-reimu`の作者である`D-Sketon`氏は、プロジェクトのmdの中でこう述べている：

> [!NOTE]
> 完全な初心者は`hugo-reimu-template`をそのまま使うことができます。リポジトリをクローンして設定を変更するだけで、基本的なブログが手に入ります！

筆者は標準的な手順に従って一から手作りしようとしたが、少し試してすぐに諦め、テンプレートプロジェクトをまるごとforkしてそれをベースに開発することにした。余計な手間が大幅に省けた（テンプレートプロジェクトと標準手順のカスタマイズ性は同じで、`D-Sketon`氏が多くのデフォルト設定を済ませてくれているだけだ）。

{{<link title="hugo-reimu-template" link="https://github.com/D-Sketon/hugo-reimu-template" cover="https://camo.githubusercontent.com/66beeb49b45f16c66f7df739279b5da72a453aa5dd3c91730c5a39fe20eee15d/68747470733a2f2f666173746c792e6a7364656c6976722e6e65742f67682f442d536b65746f6e2f626c6f672d696d672f69636f6e2e706e67">}}

templateリポジトリをforkして開発端末にpullしたら、`hugo-theme-reimu`プロジェクトのチュートリアルに従い、まず`hugo.toml`ファイルを編集して基本設定を済ませ、次に`config/_default/params.yml`を上から下へ一行ずつ修正して、既存のテンプレートを自分好みにカスタマイズしていく。~~（わからない設定はAIに聞けばいい）~~

`params.yml`の変更量はかなり多く、筆者は上から下まで一行ずつ読み込んだ。以下、ファイルの順番に沿ってすべての変更を記録する。~~（たぶん漏れはないはず）~~

### 基本情報とサブタイトル

まず`author`・`email`・`description`の三項目に自分の情報を入力する。

サブタイトルは`hugo-theme-reimu`がタイプライターアニメーションに対応しており、`subtitle.typing`以下で文章を設定できる：

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

三つの文章が順番にタイプされては消えていく。デフォルトの速度パラメータで十分良い効果が出る。`text`フィールドは`typing.enable: false`のときの静的フォールバックテキストで、こちらも合わせて変更した。

ついでに`banner_srcset`を有効にして異なる解像度のBanner画像を設定し、モバイル端末では小さいバージョンを読み込むようにした。`excerpt_link`も`継続阅读`に変更し、Blogが中国語メインであることに合わせた。

### フッターとソーシャルリンク

`footer.since`は実際の状況に合わせて`2026`に変更し、`powered`を`false`にして「Powered by Hugo」の表示を消した。

`social`フィールドに各プラットフォームのリンクを入力すると、テーマがサイドバーに対応するアイコンを自動でレンダリングする。`email`・`github`・`bilibili`・`telegram`・`steam`、そして`qq`と`weixin`を入力した（後者二つはクソ腾讯がAPIを提供していないため、友達追加用QRコードをローカルに保存して呼び出す形にした）。`网易云音乐`はテーマ内蔵のアイコンリストにないため、後で`injector`で個別に対応する必要がある（このCSSの編集は後述）。ここではリンクのみ入力してプレースホルダーとした。

### 更新日時とバッジの表示

`show_update_time`を`true`にすると、記事一覧と詳細ページに最終更新日時が追加表示される。`triangle_badge`も有効にし、アイコンを`github`、リンクを自分のプロフィールページに設定した。ページ右上角にGithubトップページへのバッジが表示される。

### フォント

本文フォントを`Noto Serif SC`（セリフ体、宋体に近い）から`Noto Sans SC`（サンセリフ体、ゴシック体に近い）に変更し、コードフォントに`JetBrains Mono`を追加した（元のフォントはWebページで読むのに向いていないと感じたため）：

```yaml
font:
  enable: true
  article:
    - Mulish
    - Noto Sans SC
  code:
    - JetBrains Mono
```

上記のフォントはすべてGoogle Fontsでホストされており、テーマが自動で読み込むため追加設定は不要だ。

### その他の機能スイッチ

`mermaid.zoom`を`true`にしてフローチャートのマウスズームに対応させた。`clipboard.copyright.content`には著作権表示のテキストを入力し、一定文字数以上をコピーした際に自動付加されるようにした（後で調べたところ、この機能はコードブロックのコピーボタンにしか効かないことがわかり、その後の修正で無効化した）。

### コメントシステム

`comment.default`を`waline`から`giscus`に変更し、`giscus`フィールドに[giscus.app](https://giscus.app/zh-CN)で生成したリポジトリ設定を入力した：

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

`giscus`は`GitHub Discussions`をベースに実装されており、コメントデータはリポジトリに保存される。サードパーティサービスが消えてしまう心配がなく、今回のバージョンで目指した「手間いらず・メンテナンスフリー」という方針にも合致している。

### プリローダー・著作権表示・投げ銭・シェア

`preloader`の各言語の読み込みテキストを、サブタイトルと呼応する文章に変更した。

`article_copyright`を有効にし、著者・タイトル・日付・更新日時・ライセンスを表示するよう設定した。ライセンスの種類は`by-nc-sa`を選択した。

`moe_icp.icpnumber`に萌国ICP番号を入力した（数字部分だけでよい）。

`sponsor`を有効にし、支付宝とWePayの受取QRコードを`static/sponsor/`ディレクトリに置き、`qr`フィールドにパスを入力した。

`share`フィールドでよく使うプラットフォームのコメントアウトをすべて解除した。記事の下部にシェアバーが表示される。

`home_categories`にはとりあえずテスト用のカテゴリを一つ入力してプレースホルダーとした。記事が増えてから整理する予定だ。

### コードインジェクション（injector）

ここが最も変更が多い部分だ。`injector.head_end`に三つの内容を注入した：
- 网易云のアイコンCSS（`mask`+SVGでアイコン形状を切り抜き、`currentColor`で色を継承してライト/ダークモードに対応）
- APlayerの固定配置スタイルの微調整、およびLive2dモデルIDの初期化スクリプト（プリセットモデルを設定してページ更新のたびにランダムに変わらないようにする）
- `injector.body_end`にはMetingJSのループボタンSVGの修正パッチを注入し、クラウドのMetingが読み込まれる際にループアイコンが消える問題を解決した。

~~（injectorのCSSとJSはほぼすべてClaude Sonnet 4.6が修正したもので、筆者には理解できない）~~

### PJAX・Live2d・音楽プレイヤー

`pjax.enable`を`true`にすると、ページ遷移が部分更新になりナビゲーションが速くなり、音楽プレイヤーもページ移動で途切れなくなる。`live2d_widgets.enable`を`true`にすると、看板娘がページ左下に表示される。

音楽プレイヤー部分では`aplayer`を有効にして自動再生（ブラウザの制限で実際には発動しないようだが）・シャッフル再生・音量0.3・リストループなどのオプションを設定し、さらに`meting`を有効にして网易云のプレイリストIDとカスタムAPIアドレスを入力した（当初はVercelにAPIを構築して自分のcookieを使っていたが、接続遅延の最適化を進める中でここがボトルネックになっていることが判明し、最終的に`injahow`が自ら管理するAPIエンドポイントを使用することにした）（ここでAPIを呼び出す記述は修正が必要で、元のままではエラーが出る）：

```yaml
meting:
  enable: true
  meting_api: "https://api.injahow.cn/meting/?server=:server&type=:type&id=:id&r=:r"
  options:
    id: 17883899120
    server: netease
    type: playlist
```

`pangu.enable`を`true`にして、中国語と英語の間に自動でスペースを挿入するようにした。~~（筆者が重度の強迫症持ちなので）~~

### テーマカラーと動的配色

オリジナルの`hugo-theme-reimu`は赤系だが、筆者は青が好みなので、`internal_theme`以下のすべての`--red-*`変数を青系の値に置き換えた。ライトモードとダークモードそれぞれ一セットずつ用意した。~~（すべての色コードはClaude Sonnet 4.6が生成した）~~変数名が`--red-*`なのはテーマのプレースホルダー命名に過ぎず、実際の色は入力した値によって決まる。

その後`material_theme`を有効にした。Banner画像から主要な色調を自動抽出して動的配色を生成するため、Bannerとの調和がより取れるようになった。~~（そのため手動で変更した色はほぼ上書きされてしまった）~~

### まとめ

以上の操作を行う際は、ローカルで`hugo server`を実行しながら繰り返しプレビューして調整した。Githubにpushしてプレビューすることもあった。満足のいく仕上がりになるまで続けた。

全体的な設定手順はGUIがないため直感的ではないが、ロジックはシンプルでわかりやすく、設定自体はそれほど難しくない。~~（これが国内開発者のプロジェクトの利点の一つだろうか）~~

> [!CAUTION]
> ファイルを変更する際は`themes/hugo-theme-reimu`フォルダ内で直接編集しないこと。`Git`の運用上のトラブルが発生する。`themes/hugo-theme-reimu`内のファイルの配置を参照し、自分の設定フォルダ内に同じ構造のフォルダを新規作成して、変更したい設定ファイルをそこにコピーしてから編集すること。

## Step 2：Github Pageへのアップロード

このステップでは、`Github Actions`がコードをpushするたびに自動でHugoサイトをビルドして`Github Pages`にデプロイするよう設定し、手動操作を省く。

`hugo-reimu-template`にはワークフローファイルが内蔵されていないため、`.github/workflows/`ディレクトリに自分で`yaml`ファイルを新規作成する必要がある。

ワークフロー全体は二つのjobに分かれている：`build`はHugoのインストール・サイトのビルド・成果物のアップロードを担当し、`deploy`は`build`の完了後に成果物を正式に`Github Pages`へ公開する。

`build` jobにはいくつか注意すべき細かい点がある：

- `checkout`時に`submodules: recursive`を追加している。テーマがサブモジュールとして導入されているため、このパラメータがないとテーマファイルを取得できない。
- `fetch-depth: 0`でgitが完全な履歴を取得するようにしている。これによりHugoが記事の`lastmod`時刻を正しく生成できる。
- HugoはSass/SCSSに対応するために`Extended`版のインストールが必要で、GitHub Releaseから直接ダウンロードして解凍し、`PATH`に追加すればよい。

```yaml
name: 構建并部署 Hugo 博客

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

ワークフローを書き終えたら、リポジトリの`Settings → Pages`で`Source`を`Github Actions`に変更する必要がある。変更しないとデプロイが何のエラーメッセージも出さずに静かに失敗する。

作業中に一つハマった点がある：最初のビルドコマンドは`hugo --gc --minify --baseURL "${{ steps.pages.outputs.base_url }}/"`と書いており、`configure-pages`というActionが`baseURL`を動的に渡してくれることを期待していた。しかし渡されてきたのが`http://`始まりのアドレスで、生成されたHTMLの絶対リンクがすべてHTTPになってしまい、HTTPSを強制する環境でmixed contentエラーが全面発生した。最終的な解決策は`--baseURL`パラメータをビルドコマンドから削除し、`hugo.toml`に`baseURL = 'https://blog.rmqg.org/'`とハードコードすることで、問題が解決した。~~（かなり長い時間を費やした）~~

## Step 3：「About」と「友達リンク」の作成

この部分の作業は`content/friend.md`と`content/about.md`の二つのファイルを作成して自分のテキストを入力することだ。また、`content/about.en.md`・`content/about.ja.md`・`content/about.zh-tw.md`などのファイルを別途作成することで、ページ右上の言語切り替え時に`关于`などの異なる言語バージョンを表示できる（筆者はClaude Sonnet 4.6を使って中国語以外の言語バージョンを翻訳した）。

## Step 4：独自ドメインの接続

以上の操作はすべてGithubのドメイン`https://rmqg.github.io/`上で行ったもので、以降の操作では独自ドメインをBlogに向けて接続パフォーマンスの最適化を行う。

### カスタムドメインのバインド

まずGithubリポジトリの`Settings → Pages → Custom domain`に`blog.rmqg.org`を入力して保存する。Githubはリポジトリのルートディレクトリに自動で`CNAME`ファイルを生成し（内容は`blog.rmqg.org`の一行）、すぐにビルドとデプロイをトリガーしてこのファイルを組み込む（最終テスト時に`rmqg.github.io`にアクセスすると実際には`rmqg.org`にリダイレクトされることが判明したが、ブラウザが廃止されたDNS解析をキャッシュしていたためと思われる。プライベートモードでは問題なかった）。

ドメインは`CloudFlare`で管理しており、DNSパネルに`CNAME`レコードを一件追加する：名前に`blog`、ターゲットに`rmqg.github.io`を入力し、右側の雲のアイコンは**グレー**のまま（つまりProxied無効、DNSのみモード）にして保存する。DNS反映を待つ——通常数分から30分程度で、その後`blog.rmqg.org`でアクセスできるようになる。

> [!TIP]
> カスタムドメインをバインドすると、`rmqg.github.io`へのアクセスはGithubによって自動的に302リダイレクトで`blog.rmqg.org`に転送される。これはGithub Pagesの内蔵ロジックであり、CloudFlareとは無関係で、別途リダイレクトルールを設定する必要はない。

Github Pagesの設定ページに戻り、GithubがDNSの正常を確認するのを待ってから`Enforce HTTPS`にチェックを入れる。GithubはLet's Encryptで証明書を自動発行し、期限前に自動更新する。ただしGithubが管理するこの証明書は秘密鍵をエクスポートできないため、後でCDNを接続する際に注意が必要だ。

> [!NOTE]
> ドメインをバインドした直後に`Enforce HTTPS`がグレーアウトしている場合は、数分待ってGithubが証明書の発行を完了すればチェックできるようになる。

### CloudFlareのオレンジ雲でアクセス高速化を検討したこと

筆者は当初CloudFlareのオレンジ雲を有効にして、CFのCDNですべてのトラフィックをプロキシする構想だった。テストしてみると、中国国内からのアクセスが非常に遅く、初回アクセスで数十秒かかってもページが部分的にしか読み込まれない（一部のCSSがレンダリングされない）ことがわかったため、別の方法を探すことにした。

そのためCloudFlareは常にグレー雲（DNSのみ）のままにして、高速化の役割を後述の国内CDNに任せることにした。

### 読み込みが遅いことに気づく

公開後、Blogの初回読み込み時間が1分近くかかることに気づいた。明らかに異常だ。F12で開発者ツールを開き、Networkパネルを確認すると、リソースリクエストがすべて`Waiting (TTFB)`で詰まっており、サーバー側のレスポンス自体が遅いことを示していた。クライアント側のレンダリングの問題ではない。

調査の手順：

1. まずDNSを確認：`nslookup blog.rmqg.org`、解析結果は正常にGithubのIPレンジを指しており、DNSに問題はない。
2. 次にサーバー側を直接テスト：`ping rmqg.github.io`、パケットロス率が高く、遅延は動かすと200〜300ms、タイムアウトすることも——**根本原因が判明した**：Github Pagesのサーバーは海外にあり、中国国内からのアクセスは遅延とパケットロス率が極めて高い。各リソースファイルのリクエストにこの遅延が発生し、ページ全体で数十のリソースがあるため、ファーストビューの読み込みが異常に遅くなるのは当然だ。

解決策の方向性は、国内にCDNレイヤーを一枚挟むことだ。ユーザーのリクエストが最寄りの国内CDNノードに届き、キャッシュがあればそのまま返し、キャッシュミスの場合のみオリジン（Github Pages）に回源して取得する。その後同じリソースへのアクセスはノードのキャッシュから直接提供され、海外を経由しなくて済む。

### 多吉云CDNの試用（Github Pagesを回源）

`多吉云`は十分な無料CDNプランがあるため選択した（筆者は一切の報酬を受け取っていない！）。

多吉云コンソールの`CDN加速 → ドメイン管理 → 加速ドメイン追加`で`blog.rmqg.org`を入力し、業務タイプを`ウェブ/ダウンロード`に選択して、回源情報を設定する：

- 回源プロトコル：`HTTPS`
- 回源アドレス：`rmqg.github.io`（Github Pagesの元のドメイン）
- 回源host：`blog.rmqg.org`

**回源hostに注意**：必ず`blog.rmqg.org`を入力すること。`rmqg.github.io`は不可。Github PagesはHostヘッダーで異なるユーザーのサイトを区別しており、CDNがGithubに回源する際のHostヘッダーが`rmqg.github.io`だと、Githubはどのリポジトリのコンテンツを返すべきかわからず、直接404になる。`blog.rmqg.org`にすることで、Githubが正しく筆者のリポジトリにルーティングできる。

同時に、CloudFlareのDNSで二つの作業を行う：

1. `_cdnauth`のTXTレコードを追加して多吉云のドメイン所有権確認を完了する（値は多吉云コンソールからコピー）。
2. `blog`のCNAMEターゲットを`rmqg.github.io`から多吉云が割り当てた`xxxxx.doge.com`形式のCNAMEエンドポイントに変更する。グレー雲はそのまま、切り替え完了。

次に多吉云にHTTPS証明書を設定する。注意点として、ここでは**Github Pagesの証明書は使えない**。あの証明書はGithubが管理するLet's Encrypt証明書で、秘密鍵は筆者の手元になく、多吉云にアップロードできる`privkey.pem`が存在しない。多吉云には`証明書無憂`という機能があり、多吉云が代わりに証明書を申請・更新してくれるため手動アップロードが不要で、筆者のような状況にぴったりだ。`HTTPS設定 → 証明書無憂`でスイッチをオンにするだけでよい。

ただし証明書無憂には注意点がある：

> システムは毎日午前中に証明書無憂サービスを有効にしているドメインの証明書の有効期限を確認し、証明書が設定されていない、または有効期限の10日以内のドメインに対して証明書の自動更新をトリガーします。

有効にしても即座には発行されず、翌朝になって初めて申請がトリガーされる。筆者は`https://blog.rmqg.org`に正常にアクセスできないまま就寝し、翌日起きて作業を再開した。

翌日のテスト結果：証明書が発行され、HTTPSでアクセスできるようになった。キャッシュがあるリソースは確かに速くなったが、**キャッシュミスの場合は依然として遅い**——CDNの回源がGithub Pagesサーバーに届く必要があり、Github側のレスポンス時間自体が長い。CDNは「すべてのユーザーが一度遅い思いをする」を「最初のユーザーだけが一度遅い思いをする」に変えるだけで、筆者のような訪問者が極めて少ない小さなBlogではキャッシュヒット率が極めて低く、実際の改善効果は非常に限定的だった。

### 多吉云COSオブジェクトストレージをオリジンに変更

根本的な解決策は、Blogの静的ファイルを多吉云自身のCOS（オブジェクトストレージ）に直接ホストし、CDNがCOSを回源とすることで、海外のGithub Pagesを完全に回避することだ。COSのサーバーは国内にあり、回源遅延は数十ミリ秒オーダーで、しかも内部ネットワークで相互接続されているため、CDNのキャッシュコールドスタート速度も大幅に向上する。

多吉云コンソールの`オブジェクトストレージ → バケット一覧 → 新規バケット作成`で、地域は国内のノードを選択する（筆者は広州在住で知人も南方が多いため広州ノードを選択）。名前は任意でよい。

作成完了後、ドメイン管理の基本設定-オリジン情報でオリジンタイプをクラウドストレージに編集し、先ほど作成したストレージスペースを選択して変更を確認する。

次にGithub Actionsのワークフローを修正し、Hugoのビルド完了・Github Pagesへの成果物アップロードの後に、`public/`ディレクトリを多吉云COSに同期アップロードするステップを追加する：

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

`DOGE_ACCESS_KEY`と`DOGE_SECRET_KEY`は多吉云アカウントのAPIキーで、多吉云コンソールの`アカウント → キー管理`で生成する。`DOGE_BUCKET`はバケット名、`DOGE_REGION`はバケットが所在する地域のコード（コンソールで確認）で、この四つの値はリポジトリの`Settings → Secrets and variables → Actions → New repository secret`でSecretとして設定する（一つずつ作成）。**ワークフローファイルに平文で書かないこと**。公開リポジトリと一緒にキーが流出してしまう。

`clean: true`というパラメータは重要だ：アップロード前にCOS内のすべての旧ファイルを先に削除してから新しくビルドしたコンテンツをアップロードする。これにより、過去の残留ファイル（削除した記事やパスを変更した画像など）がCOSに残り続けてアクセスされてしまうことを防げる。

ワークフローを修正してpushし、Actionsが完了したら多吉云COSのファイル一覧で確認する。すべてのHTML・CSS・JS・フォント・画像などのファイルが同期されているはずだ。CDNがCOSから回源するテストも問題なく、初回読み込み時間が元の数十秒から2〜3秒以内に短縮され、実測の効果は非常に顕著だった。

Github Pages側にもバックアップとして一部を残している：`Settings → Pages`で`Custom domain`を解除し、ワークフローを二回ビルドするよう変更して、それぞれ`rmqg.github.io`と`blog.rmqg.org`を`baseURL`とすることで、両方のアドレスが独立して利用可能な静的ファイルを持つようにした。CDNが落ちても`rmqg.github.io`で正常に閲覧できる。最終的に二回のビルドとデプロイの順序をより明確にするため、ワークフローを三つの直列jobに再構成した：`build（Github Pagesバージョンのビルド）→ deploy（デプロイ）→ upload-cos（COSバージョンのビルドとアップロード）`。完全なコードは末尾の付録を参照。

### ローカルのプロキシ迂回問題も処理した

ローカル開発・デバッグ時に`Clash`プロキシを使っていたところ、`blog.rmqg.org`へのトラフィックもプロキシノードを経由していることに気づいた——一度海外に出てから戻ってくる形で、国内CDNを完全に迂回しており、CDNの高速化が無意味になっていた。しかも筆者が高速化の効果を判断する際の妨げにもなっていた。

Clashのルールリストは上から下へ順番にマッチングし、最初にマッチしたルールで停止して後続のルールは確認しない。`/etc/clash/config.yaml`の`rules`フィールドの**先頭**にいくつかの`DOMAIN-SUFFIX`直接接続ルールを挿入するだけで、これらのドメインのトラフィックをプロキシを迂回して直接接続させることができる：

```yaml
- DOMAIN-SUFFIX,dogecloud.com,DIRECT
- DOMAIN-SUFFIX,dogedns.com,DIRECT
- DOMAIN-SUFFIX,dogestore.com,DIRECT
- DOMAIN-SUFFIX,rmqg.org,DIRECT
```

最初の三つは多吉云関連ドメイン（CDNエンドポイント・DNS・COSストレージ）、最後の一つは筆者自身のBlogドメインも直接接続にする。変更後にClash設定をリロード（`sudo systemstl restart clash.server`で再起動）し、再度`blog.rmqg.org`にアクセスすると直接接続になり、CDN設定の効果を検証できる。

その後のテストで、筆者が`vercel`で構築した`meting-api`がWebページの読み込みを著しく遅くしていることが判明した。Blogの安定性と保守性の向上を目指し、`injahow`が公式に管理するAPIを使用することにした：`https://injahow.github.io/meting-api/`。変更完了後、Webページ全体に素早くアクセスできるようになった。

## 終わりに

筆者は最近とても迷っている。自分に何ができるのか、何をすべきなのかがわからない。Blogを再構築してこれらの文章を書き残したのも、何か記録を残したかったからだろう。VPS上に構築したBlogは筆者がメンテナンスをやめればインターネットの記憶から消えてしまうかもしれないが、マイクロソフトのサーバーに保存されたこの数十MBのデータは、もう少し長く残り続けられると信じている。プロジェクトのメンテナンスが止まっても、後から来た人が`https://github.com/rmqg/rmqg.github.io/tree/main/content/post`の中に、ある大学生が書き残した青臭いtokenを見つけることができるだろう。

このBlogの文章が読者にとって少しでも参考になれば、助けになれば嬉しい。何か疑問があれば筆者に連絡してほしい。連絡されることは全く嫌ではない。

## 付録

その後`Github workflow`に二箇所の修正を加えた：

1. **`cancel-in-progress: false` → `true`**：元々`false`に設定していたため、短時間に連続してpushすると古いワークフローがキャンセルされず、二回の実行がどちらも`github-pages`という名前のartifactをアップロードしようとして、`deploy-pages` Actionが「Multiple artifacts named 'github-pages' were unexpectedly found」というエラーを出していた。`true`に変更することで新しいpushが古い実行を自動キャンセルするようになり、問題が解決した。

2. **ワークフローを三つのjobに再構成**：元々COSのアップロードとGithub Pagesのビルドが同じ`build` jobの中にあり、順序が混乱していた。再構成後は`build → deploy → upload-cos`の三つの直列jobになり、ロジックがより明確になった。Github Pagesのデプロイが完了してからCOSバージョンをビルドしてアップロードする。

修正後の完全なコードは以下の通り：

```yaml
name: 構建并部署 Hugo 博客

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
