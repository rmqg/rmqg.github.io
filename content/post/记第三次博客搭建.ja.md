---
title: 3回目のブログ構築記録
description: 3回目のブログ構築記録

date: 2026-04-19T11:58:32+08:00
lastmod: 2026-04-19T20:52:06+08:00
---

## はじめに
サイバーセキュリティ専攻への転入面接で話せるネタが欲しくて、長らく放置していたブログを復活させることにした。ただ、筆者はかなりの面倒くさがりなので、前の2代と同じように`WordPress+MySQL+PHP`で構築すると、サーバーの維持管理を怠ってデータを失う可能性が高い。Blog Ver.3.0を`GitHub Pages`にデプロイすれば、たとえ更新をサボっても、全記事・コメントはGitHubリポジトリに残り続けるので、サーバー期限切れによるデータロストを心配しなくて済む。

そのため、`Hugo + GitHub Actions`の組み合わせでこのブログを構築した。テーマはClaude Sonnet 4.6に勧められた二次元系テーマ`hugo-theme-reimu`を採用。

{{<link title="HUGO" link="https://gohugo.io" cover="https://github.com/gohugoio/hugo/blob/master/docs/static/apple-touch-icon.png?raw=true">}}

{{<link title="hugo-theme-reimu" link="https://github.com/D-Sketon/hugo-theme-reimu" cover="https://camo.githubusercontent.com/66beeb49b45f16c66f7df739279b5da72a453aa5dd3c91730c5a39fe20eee15d/68747470733a2f2f666173746c792e6a7364656c6976722e6e65742f67682f442d536b65746f6e2f626c6f672d696d672f69636f6e2e706e67">}}

このブログの全ファイルはパブリックリポジトリに保存されている：[https://github.com/rmqg/rmqg.github.io](https://github.com/rmqg/rmqg.github.io)、参考にどうぞ。

## Step 1：ローカル開発
`hugo-theme-reimu`の作者`D-Sketon`氏がプロジェクトのREADMEに書いていた：

> [!NOTE]
> 初心者は`hugo-reimu-template`をそのまま使えばOK。リポジトリをクローンして設定を変えるだけで基本的なブログが完成！

筆者は標準手順で一から作ろうとしたが、少し試してすぐに断念し、テンプレートプロジェクトをまるごとforkしてそこから開発を始めた。カスタマイズ性は標準手順と同じで、`D-Sketon`氏がデフォルト設定を大量に済ませてくれている分、余計な手間がかからない。

{{<link title="hugo-reimu-template" link="https://github.com/D-Sketon/hugo-reimu-template" cover="https://camo.githubusercontent.com/66beeb49b45f16c66f7df739279b5da72a453aa5dd3c91730c5a39fe20eee15d/68747470733a2f2f666173746c792e6a7364656c6976722e6e65742f67682f442d536b65746f6e2f626c6f672d696d672f69636f6e2e706e67">}}

テンプレートをforkしてローカルにpullした後は、`hugo-theme-reimu`のドキュメントに従って`hugo.toml`で基本設定を済ませ、次に`config/_default/params.yml`を上から下へ一行ずつ読みながら自分なりのカスタマイズを行う。~~（分からない設定はAIに聞けばよい）~~

`params.yml`の変更量はかなり多い。筆者は上から下まで全部読み切ったので、以下にファイルの順番通りに全変更を記録する。~~（たぶん全部書いたはず）~~

### 基本情報とサブタイトル
まず`author`・`email`・`description`の3項目を自分の情報に書き換える。

サブタイトルは`hugo-theme-reimu`がタイプライターアニメーションに対応している。`subtitle.typing`で設定：

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

3つの文がループしながら打ち込まれては消える。デフォルトの速度パラメータで十分よい仕上がりになる。`typing.enable: false`時の静的フォールバックテキストである`text`フィールドも合わせて変更。

`banner_srcset`も有効化し、解像度別のバナー画像を設定してモバイルでは小さい版を読み込むようにした。`excerpt_link`は`続きを読む`に変更。

### フッターとソーシャルリンク
`footer.since`を`2026`に変更し、`powered`を`false`に設定して「Powered by Hugo」の表示を消した。

`social`フィールドに各プラットフォームのリンクを入力するとテーマがサイドバーにアイコンを自動描画する。`email`・`github`・`bilibili`・`telegram`・`steam`と`qq`・`weixin`（テンセントがAPIを提供していないため、QRコードをローカルに保存して参照するしかない）を追加。網易云音楽はテーマのビルトインアイコンにないため、後で`injector`側でCSSを追加対応する。ここではリンクだけ記入しておく。

### 更新時刻とコーナーバッジ
`show_update_time`を`true`にすると記事一覧・詳細ページに最終更新時刻が表示される。`triangle_badge`も有効化し、アイコンを`github`にして自分のプロフィールへのリンクを設定。ページ右上にGitHubへのバッジが出るようになる。

### フォント
本文フォントを`Noto Serif SC`（セリフ体、明朝に相当）から`Noto Sans SC`（サンセリフ体、ゴシックに相当）に変更し、コードフォントに`JetBrains Mono`を追加した（デフォルトのフォントはWeb閲覧に向かないと感じたため）：

```yaml
font:
  enable: true
  article:
    - Mulish
    - Noto Sans SC
  code:
    - JetBrains Mono
```

これらはすべてGoogle Fontsでホストされており、テーマが自動で読み込むため追加設定は不要。

### その他の機能スイッチ
`mermaid.zoom`を`true`にしてフローチャートのマウスズームに対応。`clipboard.copyright.content`に著作権表示文を入力し、一定文字数以上コピーした際に自動付加されるようにした（後にこの機能はコードブロックのコピーボタンにしか効かないことが判明し、後の修正で無効化した）。

### コメントシステム
`comment.default`を`waline`から`giscus`に変更し、[giscus.app](https://giscus.app/zh-CN)で生成したリポジトリ設定を`giscus`フィールドに入力：

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

`giscus`は`GitHub Discussions`ベースなのでコメントデータがリポジトリに保存される。サードパーティサービスの突然終了を心配しなくてよいし、このバージョンのメンテナンス最小化という方針にも合致している。

### プリローダー・著作権表示・投げ銭・シェア
`preloader`の各言語の読み込みテキストをサブタイトルと呼応する文章に変更。

`article_copyright`を有効化し、著者・タイトル・日付・更新日時・ライセンスを表示するよう設定。ライセンスは`by-nc-sa`を選択。

`moe_icp.icpnumber`に萌えICP登録番号を入力（数字部分のみでよい）。

`sponsor`を有効化し、AliPayとWeChatの受取QRコードを`static/sponsor/`に置いて`qr`フィールドにパスを指定。

`share`フィールドのよく使うプラットフォームをすべてコメントアウト解除し、記事下部にシェアバーを表示。

`home_categories`にテスト用のカテゴリをひとつ追加。記事が増えたら整理する予定。

### コードインジェクション（injector）
最も雑多な変更箇所。`injector.head_end`に3つの内容を注入：
- 网易云音楽アイコン用CSS（`mask`+SVGでアイコン形状を切り抜き、`currentColor`で色を継承してライト/ダークモード両対応）
- APlayer固定配置のスタイル微調整と、Live2dモデルID初期化スクリプト（リロードのたびにモデルがランダム変更されないようプリセット）
- `injector.body_end`にMetingJSのループボタンSVG修正パッチを注入。CDNからMeting読み込み時にループアイコンが消える問題への対処。

~~（injector内のCSSとJSはほぼClaude Sonnet 4.6が書いたもので、筆者にはよく分からない）~~

### PJAX・Live2d・音楽プレイヤー

`pjax.enable`を`true`にするとページ遷移が部分更新になり、ナビゲーションが速くなり、ページ移動時に音楽プレイヤーも止まらない。`live2d_widgets.enable`を`true`にするとページ左下にマスコットキャラが出現する。

音楽プレイヤーは`aplayer`を有効化し、自動再生（ブラウザ制限で実際には動作しないようだが）・シャッフル・音量0.3・リストループを設定。`meting`も有効化し、网易云音楽のプレイリストIDとカスタムAPIアドレスを入力（当初はVercelにcookie付きのAPIを自前で立てていたが、後の最適化でそこがボトルネックと判明し、最終的に`injahow`が公式メンテナンスするAPIに切り替えた）（APIのURL形式も変更が必要で、デフォルトのままではエラーが出る）：

```yaml
meting:
  enable: true
  meting_api: "https://api.injahow.cn/meting/?server=:server&type=:type&id=:id&r=:r"
  options:
    id: 17883899120
    server: netease
    type: playlist
```

`pangu.enable`を`true`にすると中英文間に自動でスペースが挿入される。~~（筆者が重度の強迫観念持ちなので）~~

### テーマカラーとダイナミックカラー
デフォルトの`hugo-theme-reimu`は赤系。筆者は青が好みなので、`internal_theme`の`--red-*`変数をすべて青系の値に置き換えた。ライトモードとダークモードで各1セット。~~（カラーコードはすべてClaude Sonnet 4.6が生成）~~変数名が`--red-*`なのはテーマ側の仮命名で、実際の色は設定した値で決まる。

後に`material_theme`を有効化した。バナー画像から主要色を自動抽出して動的にカラーパレットを生成する機能で、バナーとの統一感が格段に上がった。~~（その結果、手動で変えた色はほぼ上書きされてしまった）~~

### まとめ

上記の作業中は`hugo server`でローカルプレビューしながら調整を繰り返した。時にはGitHubにpushして本番環境でも確認した。満足のいく仕上がりになるまで続けた。

GUIなしの設定作業は直感的でない部分もあるが、ロジック自体は明快で分かりやすい。~~（中国人開発者のプロジェクトの強みのひとつかもしれない）~~

> [!CAUTION]
> `themes/hugo-theme-reimu`フォルダ内のファイルは直接編集しないこと。Gitのトラブルの原因になる。`themes/hugo-theme-reimu`内のファイルパスを参照し、自分の設定フォルダに同じ構造でフォルダを作成してファイルをコピーし、そちらを編集すること。

## Step 2：GitHub Pagesへのデプロイ
このステップでは`GitHub Actions`を設定して、pushのたびにHugoサイトが自動ビルド・デプロイされるようにする。手動操作は一切不要になる。

`hugo-reimu-template`にはワークフローファイルが含まれていないため、自分で`.github/workflows/`にyamlファイルを作成する必要がある。

ワークフローは2つのjobで構成：`build`はHugoのインストール・サイトビルド・成果物アップロードを担当し、`deploy`は`build`完了後に成果物をGitHub Pagesに公開する。

`build` jobのいくつかの注意点：

- `checkout`に`submodules: recursive`を追加。テーマはgitサブモジュールとして組み込まれているため、これがないとテーマファイルが取得できない
- `fetch-depth: 0`でgitの完全な履歴を取得。これによりHugoが記事の`lastmod`時刻を正しく生成できる
- HugoはSass/SCSSサポートのために`Extended`版が必要。GitHub Releaseからダウンロード・展開して`PATH`に追加する

```yaml
name: Hugo ブログのビルドとデプロイ

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
      - name: コードをチェックアウト
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: Hugo Extended をインストール
        run: |
          curl -sLJO "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
          mkdir -p ~/.local/hugo
          tar -C ~/.local/hugo -xf "hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
          echo "$HOME/.local/hugo" >> $GITHUB_PATH

      - name: Pages を設定
        id: pages
        uses: actions/configure-pages@v5

      - name: サイトをビルド
        run: hugo --gc --minify

      - name: 成果物を GitHub にアップロード
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
      - name: GitHub Pages にデプロイ
        id: deployment
        uses: actions/deploy-pages@v4
```

ワークフローを書いたら、リポジトリの`Settings → Pages`で`Source`を`GitHub Actions`に変更する。これをしないとデプロイが無言で失敗する。

ひとつはまり込んだポイント：最初は`hugo --gc --minify --baseURL "${{ steps.pages.outputs.base_url }}/"`と書いて`configure-pages`に`baseURL`を動的に渡そうとした。ところが渡ってきたのが`http://`始まりのURLだったため、生成されたHTMLの絶対リンクがすべてHTTPになり、HTTPS強制環境で全面的にmixed contentエラーが発生した。修正方法は`--baseURL`フラグを削除し、`hugo.toml`に`baseURL = 'https://blog.rmqg.org/'`をハードコードすること。~~（原因を特定するまで時間がかかった）~~

## Step 3：AboutページとFriendsページの作成
`content/friend.md`と`content/about.md`を作成して自分のテキストを書くだけ。`content/about.en.md`・`content/about.ja.md`・`content/about.zh-tw.md`なども作成すれば、ページ右上の言語切り替えで各言語版のAboutが表示される（筆者は中国語以外の言語版をClaude Sonnet 4.6で翻訳した）。

## Step 4：独自ドメインの接続
ここまでの作業はすべてGitHubのドメイン`https://rmqg.github.io/`上で完結している。ここからは独自ドメインをブログに向け、接続パフォーマンスを最適化していく。

### 独自ドメインのバインド
GitHubリポジトリの`Settings → Pages → Custom domain`に`blog.rmqg.org`を入力して保存。GitHubはリポジトリルートに`CNAME`ファイル（内容は`blog.rmqg.org`の一行）を自動生成し、すぐにビルドをトリガーしてコミットする。このビルドが完了するまで他のpushはしないこと。

ドメインは`CloudFlare`で管理している。DNSパネルで`CNAME`レコードを追加：名前は`blog`、ターゲットは`rmqg.github.io`、クラウドアイコンは**グレー**のまま（Proxiedオフ、DNSのみ）。DNS反映後（通常数分〜30分）、`blog.rmqg.org`でアクセスできるようになる。

> [!TIP]
> 独自ドメインをバインドすると、`rmqg.github.io`へのアクセスはGitHubによって自動的に`blog.rmqg.org`へ302リダイレクトされる。これはGitHub Pagesの内部ロジックで、CloudFlare側の設定は不要。

GitHub Pages設定ページに戻り、DNSが正常に認識されたら`Enforce HTTPS`をチェック。GitHubがLet's Encryptの証明書を自動発行・自動更新してくれる。ただしこの証明書はGitHub管理のものでエクスポート不可。後でCDNを接続する際に注意が必要。

> [!NOTE]
> バインド直後に`Enforce HTTPS`がグレーアウトしている場合は、GitHubが証明書の発行を完了するまで数分待てばチェックできるようになる。

### CloudFlareのオレンジクラウド（CDNプロキシ）を試みた
最初はCloudFlareのクラウドをオレンジにして、CFのCDNで全トラフィックをプロキシしようと考えた。試してみると中国本土からのアクセスがかなり遅く、改善効果が限定的だったため別の方法を探すことにした。

CloudFlareのChinaネットワーク（中国本土のノードを使う本来の意味での中国向けCDN）はICP登録が必要で、個人ブログには使えない。

そのためCloudFlareは常にグレークラウド（DNSのみ）のままにし、高速化は後続の中国国内CDNに任せることにした。

### 読み込みが非常に遅いことを発見
公開後、ブログの初回読み込みが1分近くかかることが判明。明らかに異常なのでF12でデベロッパーツールを開くと、NetworkパネルでリソースリクエストがすべてWaiting (TTFB)で止まっていた。サーバーの応答自体が遅い。

調査：

1. DNSを確認：`nslookup blog.rmqg.org`、GitHubのIP範囲に正しく解決している。DNS問題なし
2. サーバーを直接テスト：`ping rmqg.github.io`、パケットロスが高く遅延も200〜300ms以上かタイムアウト。**根本原因発見**：GitHub Pagesのサーバーは海外にあるため、中国から繋ぐと地球を一周することになる。数十のリソースファイルを読み込む必要があるページでは、初回表示が遅くなるのは当然

解決策は国内CDNを前段に設置すること。ユーザーのリクエストが最寄りの中国CDNノードに届き、キャッシュがあればそのまま返す。キャッシュミス時のみオリジンへ遡って取得する。

### 多吉云CDNを試す（オリジン：GitHub Pages）
`多吉云`は無料CDN枠が十分あるため採用。~~（宣伝ではない）~~

多吉云コンソールの`CDN加速 → ドメイン管理 → ドメイン追加`で`blog.rmqg.org`を入力し、業種は`Web/ダウンロード`を選択。オリジン設定：

- オリジンプロトコル：`HTTPS`
- オリジンアドレス：`rmqg.github.io`
- オリジンhost：`blog.rmqg.org`

**オリジンhostの注意点**：必ず`blog.rmqg.org`を設定すること（`rmqg.github.io`は不可）。GitHub PagesはHostヘッダーでリポジトリを判別するため、`rmqg.github.io`で送信すると404が返る。`blog.rmqg.org`にすれば正しくルーティングされる。

HTTPS証明書の設定で注意が必要：**GitHub Pagesの証明書は使えない**。GitHubが管理するLet's Encrypt証明書であり、秘密鍵にアクセスできないため多吉云にアップロードする`privkey.pem`が存在しない。多吉云には`証書无忧（証明書安心）`機能があり、多吉云側が自動で証明書を取得・更新してくれる。`HTTPS設定 → 証書无忧`でスイッチをオンにするだけでよい。

注意点がひとつ：**システムは毎日午前中に一度だけ確認を行う**。有効化してもすぐには発行されず、翌朝まで待つ必要がある。筆者は有効化して半日待ち、その日の午後に確認したがHTTPSはまだ繋がらず、設定のどこかが間違っているのかと思って色々調べたが原因不明。そのまま寝て、翌朝起きたら証明書が発行されてサイトが正常にアクセスできるようになっていた。~~（丸一日無駄にした）~~

DNSの作業：CloudFlareで`_cdnauth`のTXTレコードを追加して多吉云のドメイン所有権を確認（値は多吉云コンソールからコピー）。確認後、`blog`のCNAMEターゲットを`rmqg.github.io`から多吉云の`xxxxx.doge.com`形式のCNAMEエンドポイントに変更。クラウドはグレーのまま。

テスト結果：キャッシュヒット時は速い。しかし**キャッシュミス時は依然として遅い**。CDNがGitHub Pagesに遡って取得する際、GitHub側の応答が遅いのは変わらない。訪問者がほぼいない個人ブログではキャッシュヒット率が低く、実質的な改善効果は限定的だった。

### 多吉云COS（オブジェクトストレージ）をオリジンに変更
根本的な解決策は静的ファイルを多吉云自身のCOS（オブジェクトストレージ）にホストし、CDNのオリジンをCOSにすること。これで海外のGitHub Pagesを完全にバイパスできる。COSは国内サーバーでレイテンシは数十ms、CDNとCOSはイントラネット接続なのでコールドスタートも高速化する。

多吉云コンソールの`オブジェクトストレージ → バケット一覧 → 新規バケット`で国内リージョンを選択（筆者は広州在住なので広州を選択）。名前は任意。

作成後、ドメイン管理の基本設定でオリジンタイプをクラウドストレージに変更し、作成したバケットを選択して保存。

GitHub Actionsワークフローを修正し、Hugoビルド後に`public/`ディレクトリを多吉云COSに同期アップロードするステップを追加：

```yaml
- name: 多吉云 COS にアップロード
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

`DOGE_ACCESS_KEY`と`DOGE_SECRET_KEY`は多吉云の`アカウント → キー管理`で生成したAPIキー。`DOGE_BUCKET`はバケット名、`DOGE_REGION`はリージョンコード（コンソールで確認）。4つすべてリポジトリの`Settings → Secrets and variables → Actions → New repository secret`に登録する。**ワークフローファイルに平文で書かない**こと。パブリックリポジトリにキーが露出してしまう。

`clean: true`は重要：アップロード前にCOS内の旧ファイルをすべて削除してから新しいビルド内容をアップロードする。削除した記事やパスを変更した画像などが残り続けるのを防ぐ。

push後、Actionsが完了したら多吉云COSのファイル一覧で全HTML・CSS・JS・フォント・画像ファイルが同期されていることを確認。CDNのCOSオリジン経由でのアクセスも正常。初回読み込み時間は1分近くから2〜3秒以内に短縮。

GitHub Pages側にもバックアップとしてコピーを保持している。`Settings → Pages`の`Custom domain`を削除した上で、ワークフローを2回ビルドするよう変更する。`rmqg.github.io`と`blog.rmqg.org`それぞれを`baseURL`にビルドすれば、どちらのアドレスも独立した静的ファイルを持つ。CDNが落ちても`rmqg.github.io`は単独で動作する。ビルドとデプロイの順序を明確にするため、最終的にワークフローを3つの直列jobに再構成した：`build（GitHub Pages版をビルド）→ deploy（デプロイ）→ upload-cos（COS版をビルドしてアップロード）`。完全なコードはこの記事末尾の付録を参照。

### ローカルのプロキシバイパス問題を修正
`Clash`でプロキシを使いながらローカル開発していると、`blog.rmqg.org`へのトラフィックもプロキシノード経由になっていることに気づいた。海外に出て戻ってくるため、国内CDNを完全に迂回してしまう。CDN設定の効果確認もできない。

Clashのルールはトップダウンマッチングで、最初にマッチした時点で停止する。`/etc/clash/config.yaml`の`rules`フィールドの**先頭**にいくつか`DOMAIN-SUFFIX`のDIRECTルールを追加するだけでよい：

```yaml
- DOMAIN-SUFFIX,dogecloud.com,DIRECT
- DOMAIN-SUFFIX,dogedns.com,DIRECT
- DOMAIN-SUFFIX,dogestore.com,DIRECT
- DOMAIN-SUFFIX,rmqg.org,DIRECT
```

最初の3つは多吉云関連ドメイン（CDNエンドポイント・DNS・COS）。最後は自分のブログドメインをダイレクト接続に。Clash設定をリロードすれば`blog.rmqg.org`がダイレクトになり、CDNの効果を正確に確認できるようになった。

後のテストで、Vercelに自前で立てていた`meting-api`がページ読み込みを大幅に遅くしていることが判明。ブログの安定性と保守性を重視して`injahow`が公式メンテナンスするAPIに切り替えた：`https://injahow.github.io/meting-api/`。変更後、ページ全体が高速に読み込まれるようになった。

## おわりに
最近、自分に何ができるのか・何をすべきなのかがよく分からなくなっている。ブログを作り直してこれを書き留めたのも、何かしらの記録を残したかったからかもしれない。VPS上のブログは更新を止めれば消えてしまうかもしれないが、マイクロソフトのサーバーに保存されているこの数十MBのデータはもう少し長く残ってくれると思う。プロジェクトの更新が止まった後も、`https://github.com/rmqg/rmqg.github.io/tree/main/content/post`には一人の大学生が書いた若々しいtokenが残り続けるはずだ。

このブログの文章が読者の何かしらの参考や助けになれば幸いです。疑問があれば気軽に連絡してください。連絡が来るのは全然嫌いではありません。

## 付録
初期設定後、`Github workflow`に2か所修正を加えた。

1. **`cancel-in-progress: false` → `true`**：もとの`false`では、短時間に連続pushすると古いワークフロー実行が取り消されず、両方が`github-pages`という名前のartifactをアップロードしてしまい、`deploy-pages` Actionが「Multiple artifacts named 'github-pages' were unexpectedly found」エラーを起こしていた。`true`に変更することで、新しいpushが古い実行を自動キャンセルするようになった。

2. **ワークフローを3 jobに再構成**：もともとCOSアップロードとGitHub Pagesビルドが同じ`build` jobに混在していて順序が不明瞭だった。`build → deploy → upload-cos`の3直列jobに再構成することで、ロジックが明確になり、GitHub Pagesのデプロイ完了後にCOS版をビルドしてアップロードするようになった。

修正後の完全なコードは以下の通り：

```yaml
name: Hugo ブログをビルドしてデプロイ

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
      - name: コードをチェックアウト
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: Hugo Extended をインストール
        run: |
          curl -sLJO "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
          mkdir -p ~/.local/hugo
          tar -C ~/.local/hugo -xf "hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
          echo "$HOME/.local/hugo" >> $GITHUB_PATH

      - name: Pages を設定
        id: pages
        uses: actions/configure-pages@v5

      - name: サイトをビルド（GitHub Pages）
        run: hugo --gc --minify --baseURL "https://rmqg.github.io/"

      - name: アーティファクトを GitHub にアップロード
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
      - name: GitHub Pages にデプロイ
        id: deployment
        uses: actions/deploy-pages@v4

  upload-cos:
    runs-on: ubuntu-latest
    needs: deploy
    env:
      HUGO_VERSION: 0.160.0
    steps:
      - name: コードをチェックアウト
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: Hugo Extended をインストール
        run: |
          curl -sLJO "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
          mkdir -p ~/.local/hugo
          tar -C ~/.local/hugo -xf "hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
          echo "$HOME/.local/hugo" >> $GITHUB_PATH

      - name: サイトをビルド（COS メインドメイン）
        run: hugo --gc --minify --baseURL "https://blog.rmqg.org/"

      - name: 多吉云 COS にアップロード
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

*翻訳は`Claude Sonnet 4.6`が提供しました*
