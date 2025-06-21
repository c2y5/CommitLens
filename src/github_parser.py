# src/github_parser.py

import requests
from collections import defaultdict
from datetime import datetime
from .cache import load_cached_data, save_to_cache, get_latest_cached_timestamp
import random

class GitHubRepoParser:
    def __init__(self, owner_repo: str, access_token: str):
        self.owner_repo = owner_repo
        self.access_tokens = access_token
        self.base_url = f"https://api.github.com/repos/{self.owner_repo}"
        self.repo_type = "gh"
        self.cache_id = self.owner_repo
        self.commits = []

    def _expand_commit(self, commit_url):
        response = requests.get(commit_url, headers={"Authorization": f"token {random.choice(self.access_tokens)}"})
        if response.status_code != 200:
            return None
        data = response.json()
        return {
            "timestamp": data["commit"]["author"]["date"],
            "author": data["commit"]["author"]["name"],
            "files": [
                {
                    "filename": f["filename"],
                    "insertions": f.get("additions", 0),
                    "deletions": f.get("deletions", 0)
                } for f in data.get("files", [])
            ]
        }

    def get_raw_commit_data_yielding(self):
        cached = load_cached_data(self.repo_type, self.cache_id)
        if cached:
            self.commits = cached
            yield f"Using cached data ({len(cached)} commits)\n"
            return

        since = get_latest_cached_timestamp(self.repo_type, self.cache_id)
        url = f"{self.base_url}/commits"
        params = {"per_page": 100, "page": 1}
        if since:
            params["since"] = since

        commits_raw = []
        page_num = 1

        while True:
            yield f"Loading page {page_num}...\n"
            response = requests.get(url, headers={"Authorization": f"token {random.choice(self.access_tokens)}"}, params=params)
            if response.status_code != 200:
                yield f"Error fetching commits: {response.status_code} - {response.text}\n"
                return
            page = response.json()
            if not page:
                break
            commits_raw.extend(page)
            params["page"] += 1
            page_num += 1

        total_commits = len(commits_raw)
        yield f"Expanding {total_commits} commits\n"

        for i, commit in enumerate(commits_raw):
            yield f"Loading commit {i + 1}/{total_commits}\n"
            expanded = self._expand_commit(commit["url"])
            if expanded:
                self.commits.append(expanded)
            if i + 1 >= 1000:
                yield "Reached commit processing limit (1000)\n"
                break

        save_to_cache(self.repo_type, self.cache_id, self.commits)

    def get_raw_commit_data(self):
        return self.commits

    def get_commit_count(self):
        return len(self.commits)

    def get_contributor_stats(self):
        stats = defaultdict(int)
        for c in self.commits:
            stats[c["author"]] += 1
        return dict(stats)
