# 自动开源到 GitHub 的 skill

**`github-auto-release`** 是一个用于自动将本地项目开源到 GitHub 的 WorkBuddy skill，内置隐私扫描、自动创建仓库、推送代码、生成多语言 README。

## 功能

- **隐私扫描**：自动检测项目中的敏感信息（token、密码、私钥、微信凭证等），防止意外泄露
- **自动创建仓库**：通过 GitHub API 创建远程仓库
- **代码推送**：自动初始化 git 并推送代码到 GitHub
- **多语言 README**：自动生成英文、中文、日文三个版本的 README

## 快速开始

```bash
python scripts/github_release.py \
  --repo "owner/repo-name" \
  --path ./project-folder \
  --token "ghp_xxxx" \
  --title "项目标题" \
  --desc "项目描述"
```

## 配置

可以通过命令行参数或环境变量配置：

```bash
# 环境变量
export GITHUB_TOKEN="ghp_xxxx"

# 运行
python scripts/github_release.py \
  --repo "owner/repo-name" \
  --path ./project-folder \
  --title "项目标题" \
  --desc "项目描述"
```

## 隐私扫描规则

自动检测并阻止上传以下敏感信息：

| 类型 | 检测模式 | 示例 |
|------|----------|------|
| GitHub Token | `ghp_`, `gho_`, `github_pat_` | `ghp_xxxx` |
| 通用 API Key | `api_key`, `apikey`, `api-key` | `api_key: "xxx"` |
| 密码/Secret | `password`, `secret`, `passwd` | `password: "xxx"` |
| 私钥文件 | `.pem`, `.key`, `id_rsa` | `id_rsa.pem` |
| 微信凭证 | `appid`, `app_secret`, `wx` | `wx1234567890` |

## 多语言 README

自动生成以下语言版本的 README：

- `README.md` - 英文
- `README.zh.md` - 中文
- `README.ja.md` - 日文

## 工作流程

1. **隐私扫描**：扫描项目目录，检测敏感文件
2. **用户确认**：展示扫描结果，要求确认
3. **创建仓库**：通过 GitHub API 创建远程仓库
4. **推送代码**：初始化 git 并推送所有代码
5. **生成 README**：根据模板生成多语言 README 并推送

## License

MIT
