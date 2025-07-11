# src/utils.py

import re

def is_github_url(s: str) -> bool:
    github_owner_repo = re.compile(r"^[\w.-]+/[\w.-]+$")
    if github_owner_repo.match(s):
        return True
    if "github.com" in s.lower():
        return True
    return False

def extract_github_repo(url: str) -> str:
    if url.startswith("github.com/"):
        url = "https://" + url

    if url.startswith("git@"):
        # git@github.com:owner/repo.git
        parts = url.split(":")
        if len(parts) > 1:
            repo_part = parts[1].lower()
            if repo_part.endswith(".git"):
                repo_part = repo_part[:-4]
            return repo_part
    else:
        # https://github.com/owner/repo or https://github.com/owner/repo.git
        parts = url.split("/")
        if len(parts) >= 5:
            owner = parts[3].lower()
            repo = parts[4].lower()
            if repo.endswith(".git"):
                repo = repo[:-4]
            return f"{owner}/{repo}"

    raise ValueError("Invalid GitHub repo URL")
