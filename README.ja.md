# GitHub Auto Release

GitHub Auto Release は、ローカルプロジェクトを自動的にGitHubにオープンソース化するWorkBuddyスキルです。プライバシースキャン、リモートリポジトリの自動作成、コードのプッシュ、多言語READMEの生成が含まれます。

## 機能

- **プライバシースキャン**：プロジェクト内の機密情報（トークン、パスワード、秘密鍵、微信認証情報など）を自動的に検出し、誤った流出を防止
- **リモートリポジトリ自動作成**：GitHub APIを使用してリモートリポジトリを作成
- **コードプッシュ**：gitを自動的に初期化し、GitHubにコードをプッシュ
- **多言語README**：英語、中国語、日本語の3つの言語バージョンのREADMEを自動生成

## クイックスタート

```bash
python scripts/github_release.py \
  --repo "owner/repo-name" \
  --path ./project-folder \
  --token "ghp_xxxx" \
  --title "プロジェクトタイトル" \
  --desc "プロジェクト説明"
```

## 設定

コマンドライン引数または環境変数で設定可能：

```bash
# 環境変数
export GITHUB_TOKEN="ghp_xxxx"

# 実行
python scripts/github_release.py \
  --repo "owner/repo-name" \
  --path ./project-folder \
  --title "プロジェクトタイトル" \
  --desc "プロジェクト説明"
```

## プライバシースキャンルール

以下の機密情報を自動的に検出し、アップロードを防止：

| タイプ | 検出パターン | 例 |
|------|----------|-----|
| GitHub Token | `ghp_`, `gho_`, `github_pat_` | `ghp_xxxx` |
| 一般 API Key | `api_key`, `apikey`, `api-key` | `api_key: "xxx"` |
| パスワード/Secret | `password`, `secret`, `passwd` | `password: "xxx"` |
| 秘密鍵ファイル | `.pem`, `.key`, `id_rsa` | `id_rsa.pem` |
| 微信認証情報 | `appid`, `app_secret`, `wx` | `wx1234567890` |

## 多言語README

以下の言語バージョンのREADMEを自動生成：

- `README.md` - 英語
- `README.zh.md` - 中国語
- `README.ja.md` - 日本語

## ワークフロー

1. **プライバシースキャン**：プロジェクトディレクトリをスキャンし、機密ファイルを検出
2. **ユーザー確認**：スキャン結果を表示し、続行確認
3. **リポジトリ作成**：GitHub APIでリモートリポジトリを作成
4. **コードプッシュ**：gitを初期化し、全コードをプッシュ
5. **README生成**：テンプレートから多言語READMEを生成し、プッシュ

## ライセンス

MIT
