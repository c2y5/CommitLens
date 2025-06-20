# src/utils.py

import os
import re

def is_github_url(s: str) -> bool:
    github_owner_repo = re.compile(r'^[\w.-]+/[\w.-]+$')
    if github_owner_repo.match(s):
        return True
    if "github.com" in s.lower():
        return True
    return False

def extract_github_repo(url: str) -> str:
    # from https://github.com/owner/repo or git@github.com:owner/repo.git
    if url.startswith("git@"):
        # git@github.com:owner/repo.git
        parts = url.split(":")
        if len(parts) > 1:
            repo_part = parts[1]
            if repo_part.endswith(".git"):
                repo_part = repo_part[:-4]
            return repo_part
    else:
        # https://github.com/owner/repo or https://github.com/owner/repo.git
        parts = url.split("/")
        if len(parts) >= 5:
            owner = parts[3]
            repo = parts[4]
            if repo.endswith(".git"):
                repo = repo[:-4]
            return f"{owner}/{repo}"
    raise ValueError("Invalid GitHub repo URL")
