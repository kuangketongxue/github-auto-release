#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Auto Release Tool
Automatically open source local projects to GitHub with privacy scanning.
Usage:
    python github_release.py --repo "owner/repo-name" --path ./project --token "ghp_xxx" --title "Title" --desc "Description"
"""
import os
import sys
import re
import json
import argparse
import subprocess
import urllib.request
import urllib.error
from pathlib import Path


# Sensitive data patterns
SENSITIVE_PATTERNS = {
    "GitHub Token": [r"ghp_[A-Za-z0-9_]{36}", r"gho_[A-Za-z0-9_]{36}", r"github_pat_[A-Za-z0-9_]{22}_[A-Za-z0-9_]{59}"],
    "API Key": [r"api[_-]?key[\"'\s:=]+[\w-]{16,}", r"apikey[\"'\s:=]+[\w-]{16,}"],
    "Password": [r"password[\"'\s:=]+[\w@#$%^&*]{6,}"],
    "Secret": [r"secret[\"'\s:=]+[\w-]{16,}"],
    "Private Key": [r"-----BEGIN (RSA |OPENSSH )?PRIVATE KEY-----"],
    "WeChat Credential": [r"wx[0-9a-f]{16,}", r"app[_-]?secret[\"'\s:=]+[\w-]{16,}"],
}

SENSITIVE_EXTENSIONS = {".pem", ".key", ".p12", ".pfx", ".id_rsa", "id_dsa"}


def scan_sensitive_files(path: str) -> list:
    """Scan for sensitive files and content."""
    issues = []
    root = Path(path)

    for file_path in root.rglob("*"):
        if not file_path.is_file():
            continue

        # Check file extension
        if file_path.suffix.lower() in SENSITIVE_EXTENSIONS or file_path.name in SENSITIVE_EXTENSIONS:
            issues.append({"file": str(file_path), "type": "Private Key File", "severity": "high"})
            continue

        # Skip binary files
        if file_path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".ico", ".zip", ".tar", ".gz", ".exe", ".dll"}:
            continue

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            for pattern_name, patterns in SENSITIVE_PATTERNS.items():
                for pattern in patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        issues.append({
                            "file": str(file_path),
                            "type": pattern_name,
                            "severity": "high",
                            "matches": len(matches)
                        })
                        break
        except Exception:
            continue

    return issues


def create_github_repo(token: str, name: str, description: str, private: bool = False) -> dict:
    """Create GitHub repository via API."""
    url = "https://api.github.com/user/repos"
    payload = json.dumps({
        "name": name,
        "description": description,
        "private": private,
        "auto_init": False
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {"success": True, "data": data}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        return {"success": False, "error": f"HTTP {e.code}: {error_body}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def init_and_push(repo_url: str, local_path: str, token: str) -> dict:
    """Initialize git repo and push to GitHub."""
    path = Path(local_path)

    # git init
    subprocess.run(["git", "init"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "github-actions@github.com"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "GitHub Actions"], cwd=path, check=True, capture_output=True)

    # git add
    subprocess.run(["git", "add", "."], cwd=path, check=True, capture_output=True)

    # git commit
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=path, check=True, capture_output=True)

    # git remote add
    remote_url = repo_url.replace("https://", f"https://{token}@")
    subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=path, check=True, capture_output=True)

    # git push
    result = subprocess.run(
        ["git", "push", "-u", "origin", "master"],
        cwd=path,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        # Try main branch
        result = subprocess.run(
            ["git", "push", "-u", "origin", "main"],
            cwd=path,
            capture_output=True,
            text=True
        )

    return {
        "success": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr
    }


def generate_readme(template_path: str, title: str, description: str, lang: str) -> str:
    """Generate README from template."""
    if not template_path or not Path(template_path).exists():
        return f"# {title}\n\n{description}\n"

    template = Path(template_path).read_text(encoding="utf-8")
    return template.replace("{{title}}", title).replace("{{description}}", description).replace("{{lang}}", lang)


def generate_xhs_caption(title: str, description: str) -> str:
    """Generate Xiaohongshu promotional caption from project info."""
    caption = f"""🔥 发现一个超棒的开源项目：{title}

{description}

✨ 为什么推荐这个项目？
• 功能强大，开箱即用
• 代码规范，易于二次开发
• 持续维护，社区活跃

💡 适合谁用？
• 想要提升效率的开发者
• 需要自动化工具的技术团队
• 对开源感兴趣的学习者

🚀 快速开始：
1. 访问 GitHub 仓库获取源码
2. 按照 README 指引安装配置
3. 开始使用，遇到问题欢迎提 Issue

---
如果觉得有用，别忘了点赞👍、收藏⭐、分享给更多朋友！
关注我，持续分享优质开源项目和技术干货。

#开源项目 #技术分享 #编程 #效率工具 #开发者
"""
    return caption.strip()


def find_cover_image(local_path: str) -> str:
    """Find a suitable cover image in the project."""
    path = Path(local_path)
    candidates = [
        "cover.png", "cover.jpg", "cover.jpeg", "cover.gif",
        "thumbnail.png", "thumbnail.jpg", "thumbnail.jpeg",
        "banner.png", "banner.jpg", "banner.jpeg",
        "icon.png", "icon.jpg", "logo.png", "logo.jpg",
    ]
    for name in candidates:
        candidate = path / name
        if candidate.exists() and candidate.is_file():
            return str(candidate)

    # Search in common subdirectories
    for subdir in ["assets", "images", "img", "media", "static"]:
        subpath = path / subdir
        if subpath.exists() and subpath.is_dir():
            for name in candidates:
                candidate = subpath / name
                if candidate.exists() and candidate.is_file():
                    return str(candidate)

    return ""


def publish_xiaohongshu_draft(title: str, cover_image: str, caption: str) -> dict:
    """Publish long-text draft to Xiaohongshu via opencli."""
    if not cover_image or not Path(cover_image).exists():
        return {"success": False, "error": "Cover image not found"}

    # Build opencli command
    cmd = ["opencli", "xiaohongshu", "publish", "--title", title, "--images", cover_image, "--draft", "--", caption]

    # Windows compatibility
    env = os.environ.copy()
    env["OPENCLI_BROWSER_COMMAND_TIMEOUT"] = "300000"
    if sys.platform == 'win32' and cmd[0] == 'opencli':
        cmd[0] = 'opencli.cmd'

    try:
        result = subprocess.run(cmd, capture_output=True, timeout=300, env=env)
        stdout = result.stdout.decode('utf-8', errors='replace') if result.stdout else ''
        stderr = result.stderr.decode('utf-8', errors='replace') if result.stderr else ''

        if "暂存成功" in stdout or "成功" in stdout or "ok: true" in stdout.lower():
            return {"success": True, "output": stdout}
        else:
            return {"success": False, "error": stderr or stdout[:200]}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "TIMEOUT"}
    except FileNotFoundError:
        return {"success": False, "error": "opencli not found. Please install opencli first."}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="GitHub Auto Release Tool")
    parser.add_argument("--repo", required=True, help="Repository name (owner/repo-name)")
    parser.add_argument("--path", default=".", help="Local project path")
    parser.add_argument("--token", help="GitHub PAT (or use GITHUB_TOKEN env)")
    parser.add_argument("--title", required=True, help="Repository title")
    parser.add_argument("--desc", default="", help="Repository description")
    parser.add_argument("--private", action="store_true", help="Create private repo")
    parser.add_argument("--readme-langs", default="en,zh,ja", help="Comma-separated README languages")
    parser.add_argument("--template", help="README template path")
    parser.add_argument("--skip-privacy-check", action="store_true", help="Skip privacy scan")
    parser.add_argument("--publish-xhs", action="store_true", help="Publish promotional text to Xiaohongshu drafts")
    parser.add_argument("--xhs-cover", help="Cover image path for Xiaohongshu post")
    args = parser.parse_args()

    # Get token
    token = args.token or os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print("Error: GitHub token required (--token or GITHUB_TOKEN env)", file=sys.stderr)
        sys.exit(1)

    local_path = Path(args.path).resolve()

    # Step 1: Privacy scan
    if not args.skip_privacy_check:
        print("[1/4] Scanning for sensitive data...")
        issues = scan_sensitive_files(str(local_path))
        if issues:
            print(f"     Found {len(issues)} potential issues:")
            for issue in issues:
                print(f"     - {issue['file']}: {issue['type']} ({issue['severity']})")
            confirm = input("     Continue anyway? (y/N): ").strip().lower()
            if confirm != "y":
                print("     Aborted.")
                sys.exit(1)
        else:
            print("     No sensitive data found.")

    # Step 2: Create GitHub repo
    print("[2/4] Creating GitHub repository...")
    repo_name = args.repo.split("/")[-1]
    result = create_github_repo(token, repo_name, args.desc, args.private)
    if not result["success"]:
        print(f"     Failed to create repo: {result['error']}", file=sys.stderr)
        sys.exit(1)
    print(f"     Created: https://github.com/{args.repo}")

    # Step 3: Push code
    print("[3/4] Pushing code...")
    repo_url = f"https://github.com/{args.repo}.git"
    push_result = init_and_push(repo_url, str(local_path), token)
    if not push_result["success"]:
        print(f"     Push failed: {push_result['stderr']}", file=sys.stderr)
        sys.exit(1)
    print("     Code pushed successfully.")

    # Step 4: Generate README
    print("[4/5] Generating multi-language README...")
    langs = [l.strip() for l in args.readme_langs.split(",")]
    for lang in langs:
        content = generate_readme(args.template, args.title, args.desc, lang)
        readme_name = f"README.{lang}.md" if lang != "en" else "README.md"
        readme_path = local_path / readme_name
        readme_path.write_text(content, encoding="utf-8")
        print(f"     Generated {readme_name}")

    # Step 5: Publish to Xiaohongshu (optional)
    if args.publish_xhs:
        print("[5/5] Publishing to Xiaohongshu drafts...")
        cover_image = args.xhs_cover or find_cover_image(str(local_path))
        if not cover_image:
            print("     Warning: No cover image found. Skipping Xiaohongshu publish.")
            print("     Provide --xhs-cover or add cover.jpg to project root.")
        else:
            caption = generate_xhs_caption(args.title, args.desc)
            result = publish_xiaohongshu_draft(args.title, cover_image, caption)
            if result["success"]:
                print("     Xiaohongshu draft published successfully.")
            else:
                print(f"     Xiaohongshu publish failed: {result['error']}", file=sys.stderr)

    print("\nDone! Repository available at:")
    print(f"  https://github.com/{args.repo}")


if __name__ == "__main__":
    main()
