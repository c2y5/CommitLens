# main.py

import sys
import os
from dotenv import load_dotenv
from src.parser import LocalGitParser
from src.github_parser import GitHubRepoParser
from src.utils import is_github_url_or_owner_repo, extract_owner_repo_from_url

def main():
    load_dotenv()
    token = os.getenv("GITHUB_API_KEY")

    if len(sys.argv) != 2:
        print("Usage: python main.py <local_repo_path_or_github_repo>")
        print("Example local path: /home/user/myrepo")
        print("Example GitHub repo: octocat/Hello-World or https://github.com/octocat/Hello-World")
        return

    user_input = sys.argv[1]

    try:
        if is_github_url_or_owner_repo(user_input):
            if "/" not in user_input:
                raise ValueError("Invalid GitHub repo format")
            if user_input.startswith("http"):
                owner_repo = extract_owner_repo_from_url(user_input)
            else:
                owner_repo = user_input
            if not token:
                print("Error: GitHub API key not found in environment variable GITHUB_API_KEY")
                return
            parser = GitHubRepoParser(owner_repo, token)
        else:
            # assume local repo path
            parser = LocalGitParser(user_input)

        print(f"✅ Total commits: {parser.get_commit_count()}")
        print(f"👤 Contributors: {parser.get_contributor_stats()}")
        print(f"📂 Top modified files:")
        for file, count in parser.get_top_modified_files():
            print(f"   {file}: {count} edits")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
