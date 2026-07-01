# {{title}}

<p align="center">
  <strong>{{description}}</strong>
</p>

<p align="center">
  <a href="https://github.com/{{repo}}/actions"><img src="https://img.shields.io/github/actions/workflow/status/{{repo}}/ci.yml?branch=main&style=for-the-badge" alt="CI"></a>
  <a href="https://github.com/{{repo}}"><img src="https://img.shields.io/github/v/release/{{repo}}?style=for-the-badge" alt="GitHub release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="License"></a>
</p>

**{{title}}** は、プライバシースキャンと多言語 README 生成を内蔵した、ローカルプロジェクトを GitHub にオープンソース化するツールです。

もし skill、プロジェクト、またはツールを GitHub に公開したい場合は、このツールを使用してください。

[GitHub](https://github.com/{{repo}}) · [バグを報告](https://github.com/{{repo}}/issues) · [機能をリクエスト](https://github.com/{{repo}}/issues)

## ハイライト

- **[プライバシースキャン](https://github.com/{{repo}}#%E3%83%97%E3%83%A9%E3%82%A4%E3%83%90%E3%82%B7%E3%83%BC%E3%82%B9%E3%82%AD%E3%83%A3%E3%83%B3)** — トークン、パスワード、秘密鍵、API キー、WeChat 認証情報を自動検出
- **[リポジトリ自動作成](https://github.com/{{repo}}#%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95)** — GitHub API でリモートリポジトリを自動作成
- **[多言語 README](https://github.com/{{repo}}#%E5%A4%9A%E8%A8%80%E8%AA%9E-readme)** — 英語、中国語、日本語の README を自動生成
- **[小红书プロモーション](https://github.com/{{repo}}#%E5%B0%8F%E7%BA%A2%E6%9B%B8%E5%AE%A3%E5%8D%8A)** — コマンド一つで宣伝文を小红书の下書きに投稿
- **[シンプルな CLI](https://github.com/{{repo}}#%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95)** — 単一の Python スクリプトで、すぐに使用可能

## インストール

**Python 3.9+** が必要です。

```bash
git clone https://github.com/{{repo}}/{{title}}.git
cd {{title}}
python scripts/github_release.py --help
```

## クイックスタート

```bash
python scripts/github_release.py \
  --repo "owner/repo-name" \
  --path ./project-folder \
  --token "ghp_xxxx" \
  --title "プロジェクトタイトル" \
  --desc "プロジェクトの説明"
```

小红书プロモーション付き：

```bash
python scripts/github_release.py \
  --repo "owner/repo-name" \
  --path ./project-folder \
  --token "ghp_xxxx" \
  --title "プロジェクトタイトル" \
  --desc "プロジェクトの説明" \
  --publish-xhs \
  --xhs-cover path/to/cover.jpg
```

## パラメータ

| パラメータ | 必須 | デフォルト | 説明 |
|-----------|----------|---------|-------------|
| `--repo` | はい | — | ターゲットリポジトリ（`owner/repo-name`） |
| `--path` | いいえ | `.` | ローカルプロジェクトパス |
| `--token` | はい* | — | GitHub PAT（または環境変数 `GITHUB_TOKEN`） |
| `--title` | はい | — | リポジトリタイトル / README 見出し |
| `--desc` | いいえ | `""` | リポジトリの説明 |
| `--private` | いいえ | `false` | プライベートリポジトリを作成 |
| `--readme-langs` | いいえ | `en,zh,ja` | README 言語（カンマ区切り） |
| `--skip-privacy-check` | いいえ | `false` | プライバシースキャンをスキップ（非推奨） |
| `--publish-xhs` | いいえ | `false` | 宣伝文を小红书の下書きに投稿 |
| `--xhs-cover` | いいえ | 自動検索 | 小红书の表紙画像パス |

## プライバシースキャン

公開前に、ツールはプロジェクトディレクトリ内の機密データをスキャンします：

| タイプ | 検出パターン | 例 |
|------|---------|---------|
| GitHub Token | `ghp_`, `gho_`, `github_pat_` | `ghp_xxxx` |
| 一般 API Key | `api_key`, `apikey`, `api-key` | `api_key: "xxx"` |
| パスワード / Secret | `password`, `secret`, `passwd` | `password: "xxx"` |
| 秘密鍵ファイル | `.pem`, `.key`, `id_rsa` | `id_rsa.pem` |
| WeChat 認証情報 | `appid`, `app_secret`, `wx` | `wx1234567890` |

問題が検出された場合、ツールは一覧を表示し、続行するかどうかユーザーに確認します。

## 多言語 README

以下が自動生成されます：

- `README.md` — 英語
- `README.zh.md` — 中国語
- `README.ja.md` — 日本語

## 小红书プロモーション

`--publish-xhs` を有効にすると、ツールは宣伝文を自動生成し、**長文下書き**として小红书に保存します（単一の表紙画像 + 長文、多画像モードではありません）。

**前提条件：** [`opencli`](https://github.com/jackwener/opencli) をインストールして設定してください。

## セキュリティ

- ソースコードにトークンをハードコードしないでください
- トークンはコマンドライン引数または環境変数で渡してください
- 公開前にプライバシースキャン結果を確認してください
- 公開後にローカルのトークンキャッシュを削除してください

## ライセンス

MIT

---

<p align="center">
  <sub><a href="https://github.com/{{repo}}">{{repo}}</a> により ❤️ で公開</sub>
</p>
