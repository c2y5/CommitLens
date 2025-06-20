# src/processing.py

from collections import defaultdict, Counter
from datetime import datetime
from typing import List, Dict, Tuple

class CommitProcessor:
    def __init__(self, commits: List[Dict]):
        self.commits = commits

    def commits_per_day(self) -> Dict[str, int]:
        counts = defaultdict(int)
        for c in self.commits:
            date = datetime.strptime(c["timestamp"], "%Y-%m-%dT%H:%M:%SZ").date()
            counts[str(date)] += 1
        return dict(sorted(counts.items()))

    def commits_per_week(self) -> Dict[str, int]:
        counts = defaultdict(int)
        for c in self.commits:
            dt = datetime.strptime(c["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
            key = f"{dt.isocalendar()[0]}-W{dt.isocalendar()[1]}"
            counts[key] += 1
        return dict(sorted(counts.items()))

    def top_contributors(self, top_n=5) -> List[Tuple[str, int]]:
        counter = Counter(c["author"] for c in self.commits)
        return counter.most_common(top_n)

    def most_edited_files(self, top_n=5) -> List[Tuple[str, int]]:
        file_counter = Counter()
        for c in self.commits:
            for f in c.get("files", []):
                file_counter[f] += 1
        return file_counter.most_common(top_n)
