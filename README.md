# GitHub Auto Release

Automatically open source local projects to GitHub with privacy scanning and multi-language README.

## Features

- Privacy scanning: automatically detect sensitive information (tokens, passwords, private keys, API keys, etc.)
- Auto-create repository via GitHub API
- Auto-initialize git and push code
- Generate multi-language README: English, Chinese, Japanese

## Quick Start

```bash
python scripts/github_release.py \
  --repo "owner/repo-name" \
  --path ./project-folder \
  --token "ghp_xxxx" \
  --title "Project Title" \
  --desc "Project description"
```

## Configuration

You can configure via command-line arguments or environment variables:

```bash
# Environment variable
export GITHUB_TOKEN="ghp_xxxx"

# Run
python scripts/github_release.py \
  --repo "owner/repo-name" \
  --path ./project-folder \
  --title "Project Title" \
  --desc "Project description"
```

## Privacy Scanning Rules

Automatically detect and prevent upload of the following sensitive information:

| Type | Detection Pattern | Example |
|------|----------|------|
| GitHub Token | `ghp_`, `gho_`, `github_pat_` | `ghp_xxxx` |
| API Key | `api_key`, `apikey`, `api-key` | `api_key: "xxx"` |
| Password/Secret | `password`, `secret`, `passwd` | `password: "xxx"` |
| Private Key Files | `.pem`, `.key`, `id_rsa` | `id_rsa.pem` |
| WeChat Credentials | `appid`, `app_secret`, `wx` | `wx1234567890` |

## Multi-language README

Automatically generate README in the following languages:

- `README.md` - English
- `README.zh.md` - Chinese
- `README.ja.md` - Japanese

## Workflow

1. **Privacy scan**: scan project directory for sensitive files
2. **User confirmation**: show scan results, ask for confirmation
3. **Create repository**: create remote repository via GitHub API
4. **Push code**: initialize git and push all code
5. **Generate README**: generate multi-language README from template and push

## License

MIT
