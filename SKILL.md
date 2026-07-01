---
name: github-auto-release
agent_created: true
description: 自动将本地项目开源到 GitHub，包含隐私数据扫描、自动创建仓库、推送代码、生成多语言 README。当用户需要将 skill、项目或工具开源到 GitHub 时使用此技能。
---

# GitHub Auto Release

自动将本地项目开源到 GitHub，内置隐私扫描和多语言 README 生成。

## 核心能力

1. **隐私扫描**：自动检测并阻止上传敏感信息（token、密码、私钥、API key 等）
2. **自动创建仓库**：通过 GitHub API 创建远程仓库
3. **代码推送**：初始化 git 并推送所有代码
4. **多语言 README**：自动生成英文、中文、日文三个版本的 README
5. **小红书宣发**：自动生成项目宣发文案并发布到小红书草稿箱（长文模式，非图文模式）

## 使用前提

1. 提供 GitHub Personal Access Token (PAT)
2. 本地项目已准备好要开源的文件
3. 确认项目不包含需要保密的敏感数据

## 快速开始

```bash
python scripts/github_release.py \
  --repo "owner/repo-name" \
  --path ./project-folder \
  --token "ghp_xxxx" \
  --title "Project Title" \
  --desc "Project description"
```

## 参数说明

- `--repo`：目标仓库名（格式：`owner/repo-name`）
- `--path`：本地项目路径（默认：当前目录）
- `--token`：GitHub PAT（也可通过环境变量 `GITHUB_TOKEN` 传入）
- `--title`：仓库标题
- `--desc`：仓库描述
- `--private`：创建私有仓库（默认：false，公开）
- `--readme-langs`：README 语言版本，逗号分隔（默认：en,zh,ja）
- `--skip-privacy-check`：跳过隐私扫描（不推荐）
- `--publish-xhs`：发布宣发文案到小红书草稿箱（长文模式，非图文模式）
- `--xhs-cover`：小红书封面图路径（可选，默认自动查找项目中的 cover.jpg 等）

## 隐私扫描规则

自动检测并阻止以下敏感信息上传：

| 类型 | 检测模式 | 示例 |
|------|----------|------|
| GitHub Token | `ghp_`, `gho_`, `github_pat_` | `ghp_xxxx` |
| 通用 API Key | `api_key`, `apikey`, `api-key` | `api_key: "xxx"` |
| 密码/Secret | `password`, `secret`, `passwd` | `password: "xxx"` |
| 私钥文件 | `.pem`, `.key`, `id_rsa` | `id_rsa.pem` |
| 微信凭证 | `appid`, `app_secret`, `wx` | `wx1234567890` |

扫描结果会列出所有可疑文件，要求用户确认后再继续。

## 多语言 README

自动生成以下语言版本的 README：

- `README.en.md` - 英文
- `README.zh.md` - 中文
- `README.ja.md` - 日文

如果仓库已有 README，会自动追加缺失的语言版本。

## 工作流程

1. **隐私扫描**：扫描项目目录，检测敏感文件
2. **用户确认**：展示扫描结果，要求确认
3. **创建仓库**：通过 GitHub API 创建远程仓库
4. **初始化 Git**：`git init` → `git add` → `git commit` → `git remote add` → `git push`
5. **生成 README**：根据模板生成多语言 README 并推送
6. **小红书宣发**（可选）：生成项目宣发文案，自动发布到小红书草稿箱（长文模式）

## 模板

使用项目根目录的 `README.template.md` 作为 README 模板，变量替换：
- `{{title}}` - 仓库标题
- `{{description}}` - 仓库描述
- `{{lang}}` - 语言代码（en/zh/ja）

## 安全注意事项

- 永远不要在代码中硬编码 token
- 使用环境变量或命令行参数传入 token
- 推送前必须经过隐私扫描
- 推送后立即清理本地 token 缓存

## 小红书宣发（可选）

开源项目时可同时发布宣发文案到小红书草稿箱，吸引更多用户关注。

### 使用方式

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

### 参数说明

- `--publish-xhs`：启用小红书宣发功能
- `--xhs-cover`：指定封面图路径（可选）。如果不指定，自动在项目根目录查找 `cover.jpg`、`thumbnail.png`、`logo.png` 等常见文件名

### 宣发文案生成

自动从项目标题和描述生成小红书风格文案，包含：
- 项目介绍
- 核心卖点
- 适用人群
- 快速开始指引
- 互动引导

### 发布方式

通过 `opencli xiaohongshu publish` 发布为**长文草稿**（单张封面图 + 长文案），而非多图图文模式。

前置依赖：需安装并配置 `opencli`。

## 资源引用

- 详细 API 参数见 references/github_api.md
- README 模板见 `references/readme_template.{en,zh,ja}.md`
