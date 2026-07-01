# {{title}}

<p align="center">
  <strong>{{description}}</strong>
</p>

<p align="center">
  <a href="https://github.com/{{repo}}/actions"><img src="https://img.shields.io/github/actions/workflow/status/{{repo}}/ci.yml?branch=main&style=for-the-badge" alt="CI"></a>
  <a href="https://github.com/{{repo}}"><img src="https://img.shields.io/github/v/release/{{repo}}?style=for-the-badge" alt="GitHub release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="License"></a>
</p>

**{{title}}** 自动将本地项目开源到 GitHub，内置隐私扫描与多语言 README 生成。

如果你希望通过一条命令将 skill、项目或工具发布到 GitHub，这个工具就是为此设计的。

[GitHub](https://github.com/{{repo}}) · [报告 Bug](https://github.com/{{repo}}/issues) · [请求功能](https://github.com/{{repo}}/issues)

## 核心功能

- **[隐私扫描](https://github.com/{{repo}}#隐私扫描)** — 发布前自动检测 token、密码、私钥、API key 和微信凭证
- **[自动创建仓库](https://github.com/{{repo}}#快速开始)** — 通过 GitHub API 一条命令创建远程仓库
- **[多语言 README](https://github.com/{{repo}}#多语言-readme)** — 自动生成英文、中文、日文 README
- **[小红书宣发](https://github.com/{{repo}}#小红书宣发)** — 一条命令发布推广文案到小红书草稿箱
- **[简洁 CLI](https://github.com/{{repo}}#快速开始)** — 单个 Python 脚本，开箱即用

## 安装

需要 **Python 3.9+**。

```bash
git clone https://github.com/{{repo}}/{{title}}.git
cd {{title}}
python scripts/github_release.py --help
```

## 快速开始

```bash
python scripts/github_release.py \
  --repo "owner/repo-name" \
  --path ./project-folder \
  --token "ghp_xxxx" \
  --title "项目标题" \
  --desc "项目描述"
```

带小红书宣发：

```bash
python scripts/github_release.py \
  --repo "owner/repo-name" \
  --path ./project-folder \
  --token "ghp_xxxx" \
  --title "项目标题" \
  --desc "项目描述" \
  --publish-xhs \
  --xhs-cover path/to/cover.jpg
```

## 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|-----------|----------|---------|-------------|
| `--repo` | 是 | — | 目标仓库（格式：`owner/repo-name`） |
| `--path` | 否 | `.` | 本地项目路径 |
| `--token` | 是* | — | GitHub PAT（也可通过环境变量 `GITHUB_TOKEN` 传入） |
| `--title` | 是 | — | 仓库标题 / README 标题 |
| `--desc` | 否 | `""` | 仓库描述 |
| `--private` | 否 | `false` | 创建私有仓库 |
| `--readme-langs` | 否 | `en,zh,ja` | README 语言版本，逗号分隔 |
| `--skip-privacy-check` | 否 | `false` | 跳过隐私扫描（不推荐） |
| `--publish-xhs` | 否 | `false` | 发布推广文案到小红书草稿箱 |
| `--xhs-cover` | 否 | 自动查找 | 小红书封面图路径 |

## 隐私扫描

发布前，工具会扫描项目目录中的敏感数据：

| 类型 | 检测模式 | 示例 |
|------|---------|---------|
| GitHub Token | `ghp_`, `gho_`, `github_pat_` | `ghp_xxxx` |
| 通用 API Key | `api_key`, `apikey`, `api-key` | `api_key: "xxx"` |
| 密码 / Secret | `password`, `secret`, `passwd` | `password: "xxx"` |
| 私钥文件 | `.pem`, `.key`, `id_rsa` | `id_rsa.pem` |
| 微信凭证 | `appid`, `app_secret`, `wx` | `wx1234567890` |

如果发现敏感信息，工具会列出问题并等待用户确认后再继续。

## 多语言 README

自动生成以下文件：

- `README.md` — 英文
- `README.zh.md` — 中文
- `README.ja.md` — 日文

## 小红书宣发

启用 `--publish-xhs` 后，工具会自动生成推广文案，并以**长文草稿**形式保存到小红书（单张封面图 + 长文案，非多图图文模式）。

**前置依赖：** 需要安装并配置 [`opencli`](https://github.com/jackwener/opencli)。

## 安全注意事项

- 永远不要在代码中硬编码 token
- 通过命令行参数或环境变量传入 token
- 发布前务必查看隐私扫描结果
- 发布后清理本地 token 缓存

## 许可证

MIT

---

<p align="center">
  <sub>由 <a href="https://github.com/{{repo}}">{{repo}}</a> 用 ❤️ 发布</sub>
</p>
