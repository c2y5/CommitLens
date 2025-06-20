# src/github_parser.py

import requests
from collections import defaultdict
from datetime import datetime

class GitHubRepoParser:
    def __init__(self, owner_repo: str, access_token: str):
        self.owner_repo = owner_repo
        self.headers = {"Authorization": f"token {access_token}"}
        self.base_url = f"https://api.github.com/repos/{self.owner_repo}"
        self.commits = []
        self._fetch_all_commits()

    def _fetch_all_commits(self):
        commits_url = f"{self.base_url}/commits"
        params = {"per_page": 100, "page": 1}
        commits = []

        while True:
            response = requests.get(commits_url, headers=self.headers, params=params)
            if response.status_code != 200:
                raise ValueError(f"GitHub API error: {response.status_code} - {response.text}")

            page_commits = response.json()
            if not page_commits:
                break

            commits.extend(page_commits)
            params["page"] += 1

        self.commits = commits

    def get_commit_count(self):
        return len(self.commits)

    def get_contributor_stats(self):
        stats = defaultdict(int)
        for c in self.commits:
            author = c["commit"]["author"]["name"]
            stats[author] += 1
        return dict(stats)

    def get_top_modified_files(self, top_n=10):
        file_counter = defaultdict(int)
        for i, c in enumerate(self.commits):
            commit_url = c["url"]
            response = requests.get(commit_url, headers=self.headers)
            if response.status_code != 200:
                continue
            commit_data = response.json()
            files = commit_data.get("files", [])
            for f in files:
                filename = f.get("filename")
                if filename:
                    file_counter[filename] += 1
            if i >= 1000:
                break
        sorted_files = sorted(file_counter.items(), key=lambda x: x[1], reverse=True)
        return sorted_files[:top_n]

    def get_raw_commit_data(self):
        data = []
        for i, commit in enumerate(self.commits):
            entry = {
                "timestamp": commit["commit"]["author"]["date"],
                "author": commit["commit"]["author"]["name"],
                "files": []
            }

            commit_url = commit["url"]
            response = requests.get(commit_url, headers=self.headers)
            if response.status_code == 200:
                commit_data = response.json()
                entry["files"] = [f["filename"] for f in commit_data.get("files", [])]

            data.append(entry)
            if i >= 1000:
                break

        return data
    