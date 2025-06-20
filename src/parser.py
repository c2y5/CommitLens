# src/parser.py

from git import Repo
from collections import defaultdict
from datetime import datetime
import os
import pathspec

class LocalGitParser():
    def __init__(self, repo_path: str):
        if not os.path.isdir(repo_path):
            raise ValueError("Invalid local path")
        self.repo_path = repo_path
        self.repo = Repo(repo_path)
        if self.repo.bare:
            raise ValueError("Bare repo not supported")
        self.commits = list(self.repo.iter_commits())

        # Load .gitignore patterns from repo root
        gitignore_path = os.path.join(repo_path, ".gitignore")
        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r") as f:
                gitignore_content = f.read().splitlines()
            self.ignore_spec = pathspec.PathSpec.from_lines("gitwildmatch", gitignore_content)
        else:
            self.ignore_spec = pathspec.PathSpec.from_lines("gitwildmatch", [])

    def _is_ignored(self, filepath):
        rel_path = filepath.replace(os.sep, '/')
        return self.ignore_spec.match_file(rel_path)

    def get_commit_count(self):
        return len(self.commits)

    def get_contributor_stats(self):
        stats = defaultdict(int)
        for commit in self.commits:
            stats[commit.author.name] += 1
        return dict(stats)

    def get_top_modified_files(self, top_n=10):
        file_counter = defaultdict(int)
        for commit in self.commits:
            try:
                for file in commit.stats.files:
                    if not self._is_ignored(file):
                        file_counter[file] += 1
            except Exception:
                continue
        sorted_files = sorted(file_counter.items(), key=lambda x: x[1], reverse=True)
        return sorted_files[:top_n]

    def get_raw_commit_data(self):
        data = []
        for commit in self.commits:
            timestamp = datetime.fromtimestamp(commit.committed_date).strftime("%Y-%m-%dT%H:%M:%SZ")
            author = commit.author.name
            # Filter files with .gitignore
            files = [f for f in commit.stats.files.keys() if not self._is_ignored(f)]
            data.append({
                "timestamp": timestamp,
                "author": author,
                "files": files
            })
        return data
