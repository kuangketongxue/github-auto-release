# {{title}}

<p align="center">
  <strong>{{description}}</strong>
</p>

<p align="center">
  <a href="https://github.com/{{repo}}/actions"><img src="https://img.shields.io/github/actions/workflow/status/{{repo}}/ci.yml?branch=main&style=for-the-badge" alt="CI"></a>
  <a href="https://github.com/{{repo}}"><img src="https://img.shields.io/github/v/release/{{repo}}?style=for-the-badge" alt="GitHub release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="License"></a>
</p>

**{{title}}** automatically open sources local projects to GitHub with built-in privacy scanning and multi-language README generation.

If you want to publish a skill, project, or tool to GitHub with a single command, this is it.

[GitHub](https://github.com/{{repo}}) · [Report Bug](https://github.com/{{repo}}/issues) · [Request Feature](https://github.com/{{repo}}/issues)

## Highlights

- **[Privacy Scanner](https://github.com/{{repo}}#privacy-scan)** — automatically detects tokens, passwords, private keys, API keys, and WeChat credentials before publishing
- **[Auto-create Repository](https://github.com/{{repo}}#usage)** — creates GitHub repository via API with one command
- **[Multi-language README](https://github.com/{{repo}}#multi-language-readme)** — generates English, Chinese, and Japanese README files automatically
- **[Xiaohongshu Promotion](https://github.com/{{repo}}#xiaohongshu-promotion)** — publishes promotional draft to Xiaohongshu with a single flag
- **[Simple CLI](https://github.com/{{repo}}#usage)** — single Python script with sensible defaults

## Install

Requires **Python 3.9+**.

```bash
git clone https://github.com/{{repo}}/{{title}}.git
cd {{title}}
python scripts/github_release.py --help
```

## Quick Start

```bash
python scripts/github_release.py \
  --repo "owner/repo-name" \
  --path ./project-folder \
  --token "ghp_xxxx" \
  --title "Project Title" \
  --desc "Project description"
```

With Xiaohongshu promotion:

```bash
python scripts/github_release.py \
  --repo "owner/repo-name" \
  --path ./project-folder \
  --token "ghp_xxxx" \
  --title "Project Title" \
  --desc "Project description" \
  --publish-xhs \
  --xhs-cover path/to/cover.jpg
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--repo` | Yes | — | Target repository (`owner/repo-name`) |
| `--path` | No | `.` | Local project path |
| `--token` | Yes* | — | GitHub PAT (or use `GITHUB_TOKEN` env) |
| `--title` | Yes | — | Repository title / README heading |
| `--desc` | No | `""` | Repository description |
| `--private` | No | `false` | Create private repository |
| `--readme-langs` | No | `en,zh,ja` | Comma-separated README languages |
| `--skip-privacy-check` | No | `false` | Skip privacy scan (not recommended) |
| `--publish-xhs` | No | `false` | Publish promotional draft to Xiaohongshu |
| `--xhs-cover` | No | auto | Cover image path for Xiaohongshu post |

## Privacy Scan

Before publishing, the tool scans the project directory for sensitive data:

| Type | Pattern | Example |
|------|---------|---------|
| GitHub Token | `ghp_`, `gho_`, `github_pat_` | `ghp_xxxx` |
| API Key | `api_key`, `apikey`, `api-key` | `api_key: "xxx"` |
| Password / Secret | `password`, `secret`, `passwd` | `password: "xxx"` |
| Private Key File | `.pem`, `.key`, `id_rsa` | `id_rsa.pem` |
| WeChat Credential | `appid`, `app_secret`, `wx` | `wx1234567890` |

If issues are found, the tool lists them and asks for confirmation before proceeding.

## Multi-language README

Automatically generates:

- `README.md` — English
- `README.zh.md` — Chinese
- `README.ja.md` — Japanese

## Xiaohongshu Promotion

When `--publish-xhs` is enabled, the tool automatically generates a promotional caption and saves it as a long-text draft in Xiaohongshu (single cover image + caption, not multi-image mode).

**Prerequisite:** Install and configure [`opencli`](https://github.com/jackwener/opencli).

## Security

- Never hardcode tokens in source code
- Pass tokens via command-line arguments or environment variables
- Always review privacy scan results before confirming
- Delete local token references after publishing

## License

MIT

---

<p align="center">
  <sub>Released with ❤️ by <a href="https://github.com/{{repo}}">{{repo}}</a></sub>
</p>
