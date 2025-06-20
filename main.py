# main.py
import os
import sys
from dotenv import load_dotenv

from src.parser import LocalGitParser
from src.github_parser import GitHubRepoParser
from src.processing import CommitProcessor
from src.utils import is_github_url, extract_github_repo
from src.visualiser import plot_line_graph, plot_bar_chart, plot_pie_chart
from src.cache import load_cached_data, save_to_cache
from src.ui import ChartViewer

def main():
    load_dotenv()
    token = os.getenv("GITHUB_API_KEY")

    if len(sys.argv) != 2:
        print("Usage: python main.py <local_repo_path_or_github_repo>")
        print("Example: ./my-repo or octocat/Hello-World")
        return

    user_input = sys.argv[1]

    try:
        if is_github_url(user_input):
            repo_type = "gh"
            if user_input.startswith("http"):
                identifier = extract_github_repo(user_input)
            else:
                identifier = user_input
            if not token:
                print("❌ GitHub token not found in .env (GITHUB_API_KEY).")
                return
            parser = GitHubRepoParser(identifier, token)
        else:
            repo_type = "local"
            identifier = os.path.abspath(user_input)
            parser = LocalGitParser(identifier)

        raw_commits = load_cached_data(repo_type, identifier)
        if not raw_commits:
            print("🔁 Cache expired or not found. Fetching fresh data...")
            raw_commits = parser.get_raw_commit_data()
            save_to_cache(repo_type, identifier, raw_commits)
        else:
            print("✅ Using cached commit data.")

        processor = CommitProcessor(raw_commits)

        # Processed data
        daily = processor.commits_per_day()
        weekly = processor.commits_per_week()
        contributors = dict(processor.top_contributors())
        top_files = dict(processor.most_edited_files())

        figures = [
            plot_line_graph(daily, "Commits Per Day", "Date", "Commits"),
            plot_line_graph(weekly, "Commits Per Week", "Week", "Commits"),
            plot_bar_chart(top_files, "Top Edited Files", "File", "Edits"),
            plot_pie_chart(contributors, "Top Contributors"),
        ]

        ChartViewer(figures, chart_dir="charts", repo_type=repo_type, identifier=identifier)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
