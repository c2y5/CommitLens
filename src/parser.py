# src/parser.py

from git import Repo
from collections import defaultdict
from datetime import datetime
import os

class BaseGitParser:
    def get_commit_count(self):
        raise NotImplementedError()

    def get_contributor_stats(self):
        raise NotImplementedError()

    def get_top_modified_files(self, top_n=10):
        raise NotImplementedError()


class LocalGitParser(BaseGitParser):
    def __init__(self, repo_path: str):
        if not os.path.isdir(repo_path):
            raise ValueError("Invalid local path")
        self.repo = Repo(repo_path)
        if self.repo.bare:
            raise ValueError("Bare repo not supported")
        self.commits = list(self.repo.iter_commits())

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
                    file_counter[file] += 1
            except Exception:
                continue
        sorted_files = sorted(file_counter.items(), key=lambda x: x[1], reverse=True)
        return sorted_files[:top_n]
