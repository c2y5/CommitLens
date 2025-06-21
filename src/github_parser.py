# src/github_parser.py

import requests
from collections import defaultdict
from .cache import load_cached_data, save_to_cache, get_latest_cached_timestamp
import concurrent.futures
import time

class GitHubRepoParser:
    def __init__(self, owner_repo: str, access_token: list):
        self.owner_repo = owner_repo
        self.access_tokens = access_token
        self.base_url = f"https://api.github.com/repos/{self.owner_repo}"
        self.repo_type = "gh"
        self.cache_id = self.owner_repo
        self.commits = []

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
            response = requests.get(
                url,
                headers={"Authorization": f"token {self.access_tokens[page_num % len(self.access_tokens)]}"},
                params=params
            )
            if response.status_code != 200:
                yield f"Error fetching commits: {response.status_code} - {response.text}\n"
                
                if response.status_code == 403 and "X-RateLimit-Remaining" in response.headers:
                    yield f"[Rate Limit]\n"
                return 2
            page = response.json()
            if not page:
                break
            commits_raw.extend(page)
            params["page"] += 1
            page_num += 1

        total_commits = min(1000, len(commits_raw))
        yield f"Expanding {total_commits} commits using {len(self.access_tokens)} threads\n"

        def thread_worker(commit_url, token, retries=3):
            for attempt in range(retries):
                try:
                    response = requests.get(commit_url, headers={"Authorization": f"token {token}"})
                    if response.status_code == 200:
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
                    else:
                        print(f"[Warning] Token ****{token[-4:]} failed: {response.status_code} for {commit_url}")
                        if response.status_code == 403 and "X-RateLimit-Remaining" in response.headers:
                            print("[Rate Limit] Remaining:", response.headers["X-RateLimit-Remaining"])
                except Exception as e:
                    print(f"[Error] {e} on {commit_url}")
                time.sleep(1)
            return None

        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.access_tokens)) as executor:
            futures = [
                executor.submit(
                    thread_worker, commit["url"], self.access_tokens[i % len(self.access_tokens)]
                )
                for i, commit in enumerate(commits_raw[:1000])
            ]
            concurrent.futures.wait(futures)

            for i, future in enumerate(futures):
                result = future.result()
                if result:
                    self.commits.append(result)

                elapsed = time.time() - start_time
                completed = i + 1
                remaining = total_commits - completed
                avg_time = elapsed / completed if completed else 0
                eta_seconds = int(avg_time * remaining)
                eta_min, eta_sec = divmod(eta_seconds, 60)

                yield f"Processed commit {completed}/{total_commits} — ETA: {eta_min}m {eta_sec}s\n"

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
