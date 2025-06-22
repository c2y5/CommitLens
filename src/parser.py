# src/parser.py

from git import Repo
from collections import defaultdict
from datetime import datetime
import os
import pathspec
from .cache import load_cached_data, save_to_cache, get_latest_cached_timestamp

class LocalGitParser:
    def __init__(self, repo_path: str):
        if not os.path.isdir(repo_path):
            raise ValueError("Invalid local path")
        self.repo_path = repo_path
        self.repo = Repo(repo_path)
        if self.repo.bare:
            raise ValueError("Bare repo not supported")

        self.repo_type = "local"
        self.cache_id = os.path.abspath(repo_path)
        self.commits = []

        gitignore_path = os.path.join(repo_path, ".gitignore")
        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r") as f:
                lines = f.read().splitlines()
            self.ignore_spec = pathspec.PathSpec.from_lines("gitwildmatch", lines)
        else:
            self.ignore_spec = pathspec.PathSpec.from_lines("gitwildmatch", [])

    def _is_ignored(self, filepath):
        return self.ignore_spec.match_file(filepath.replace(os.sep, "/"))

    def get_raw_commit_data_yielding(self):
        cached = load_cached_data(self.repo_type, self.cache_id)
        if cached:
            self.commits = cached
            yield f"Using cached data ({len(cached)} commits)\n"
            return

        since_ts = get_latest_cached_timestamp(self.repo_type, self.cache_id)
        commits = list(self.repo.iter_commits())
        commits.reverse()

        total = len(commits)
        yield f"Found {total} new commits\n"

        for i, commit in enumerate(commits):
            ts = datetime.fromtimestamp(commit.committed_date).strftime("%Y-%m-%dT%H:%M:%SZ")
            if since_ts and ts <= since_ts:
                continue
            files = []
            for f, stats in commit.stats.files.items():
                if self._is_ignored(f):
                    continue
                files.append({
                    "filename": f,
                    "insertions": stats.get("insertions", 0),
                    "deletions": stats.get("deletions", 0)
                })
            self.commits.append({
                "timestamp": ts,
                "author": commit.author.name,
                "files": files
            })
            yield f"{i + 1}/{total} commits loaded\n"
            if i + 1 >= 1000:
                yield "Reached commit processing limit (1000)\n"
                break

        save_to_cache(self.repo_type, self.cache_id, self.commits)

        cached = load_cached_data(self.repo_type, self.cache_id)
        if cached:
            self.commits = cached
            yield f"Using cached data ({len(cached)} commits)\n"

    def get_raw_commit_data(self):
        return self.commits

    def get_commit_count(self):
        return len(self.commits)

    def get_contributor_stats(self):
        stats = defaultdict(int)
        for c in self.commits:
            stats[c["author"]] += 1
        return dict(stats)
