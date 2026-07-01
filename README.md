# GitHub Auto Release

<p align="center">
  <strong>Automatically open source local projects to GitHub with built-in privacy scanning, multi-language README generation, and Xiaohongshu promotion.</strong>
</p>

<p align="center">
  <a href="https://github.com/binlo/github-auto-release/actions"><img src="https://img.shields.io/github/actions/workflow/status/binlo/github-auto-release/ci.yml?branch=main&style=for-the-badge" alt="CI"></a>
  <a href="https://github.com/binlo/github-auto-release"><img src="https://img.shields.io/github/v/release/binlo/github-auto-release?style=for-the-badge" alt="GitHub release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="License"></a>
</p>

**GitHub Auto Release** is a CLI tool that publishes local projects to GitHub in one command. It scans for sensitive data, creates the repository via API, pushes the code, generates multi-language READMEs, and optionally promotes the project on Xiaohongshu.

If you want a repeatable, privacy-safe open-source workflow that does not require manual GitHub setup, this is it.

[GitHub](https://github.com/binlo/github-auto-release) · [Report Bug](https://github.com/binlo/github-auto-release/issues) · [Request Feature](https://github.com/binlo/github-auto-release/issues)

## Highlights

- **[Privacy-first Scanner](https://github.com/binlo/github-auto-release#privacy-scan)** — blocks tokens, passwords, private keys, API keys, and WeChat credentials before any data leaves your machine
- **[GitHub API Integration](https://github.com/binlo/github-auto-release#quick-start)** — creates repos, uploads code, and manages materials without browser automation
- **[Multi-language README](https://github.com/binlo/github-auto-release#multi-language-readme)** — generates English, Chinese, and Japanese READMEs from templates
- **[Xiaohongshu Promotion](https://github.com/binlo/github-auto-release#xiaohongshu-promotion)** — publishes a long-form promotional draft with one flag
- **[Simple CLI](https://github.com/binlo/github-auto-release#quick-start)** — single Python script with sensible defaults

## Install

Requires **Python 3.9+**.

```bash
git clone https://github.com/binlo/github-auto-release.git
cd github-auto-release
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

| Type | Detection Pattern | Example |
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

When `--publish-xhs` is enabled, the tool automatically generates a promotional caption and saves it as a long-form draft in Xiaohongshu (single cover image + caption, not multi-image mode).

**Prerequisite:** Install and configure [`opencli`](https://github.com/jackwener/opencli).

## Workflow

1. **Privacy scan**: scan project directory for sensitive files
2. **User confirmation**: show scan results, ask for confirmation
3. **Create repository**: create remote repository via GitHub API
4. **Push code**: initialize git and push all code
5. **Generate README**: generate multi-language README from template and push
6. **Xiaohongshu promotion** (optional): generate promotional text and publish draft

## Security

- Never hardcode tokens in source code
- Pass tokens via command-line arguments or environment variables
- Always review privacy scan results before confirming
- Delete local token references after publishing

## License

MIT

---

<p align="center">
  <sub>Released with ❤️ by <a href="https://github.com/binlo/github-auto-release">github-auto-release</a></sub>
</p>
