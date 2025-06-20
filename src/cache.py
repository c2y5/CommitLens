# src/cache.py

import os
import json
from datetime import datetime, timedelta

CACHE_FILE = "cache/data.json"
CACHE_AGE_LIMIT = timedelta(hours=4)

def _load_all_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def _save_all_cache(all_data):
    os.makedirs("cache", exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(all_data, f, indent=2)

def _make_cache_key(repo_type: str, identifier: str) -> str:
    return f"{repo_type}:{identifier}"  # e.g. "gh:octocat/Hello-World" or "local:/path/to/repo"

def load_cached_data(repo_type: str, identifier: str):
    key = _make_cache_key(repo_type, identifier)
    all_cache = _load_all_cache()
    if key not in all_cache:
        return None
    entry = all_cache[key]
    timestamp = datetime.fromisoformat(entry["timestamp"])
    if datetime.utcnow() - timestamp > CACHE_AGE_LIMIT:
        return None
    return entry["commits"]

def save_to_cache(repo_type: str, identifier: str, commits):
    key = _make_cache_key(repo_type, identifier)
    all_cache = _load_all_cache()
    all_cache[key] = {
        "timestamp": datetime.utcnow().isoformat(),
        "commits": commits
    }
    _save_all_cache(all_cache)

def delete_cache(repo_type=None, identifier=None):
    if not os.path.exists(CACHE_FILE):
        return False
    if not repo_type or not identifier:
        os.remove(CACHE_FILE)
        return True

    key = _make_cache_key(repo_type, identifier)
    all_cache = _load_all_cache()
    if key in all_cache:
        del all_cache[key]
        _save_all_cache(all_cache)
        return True
    return False
