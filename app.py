from flask import Flask, render_template, request, redirect, url_for, flash
import os
from dotenv import load_dotenv

from src.parser import LocalGitParser
from src.github_parser import GitHubRepoParser
from src.processing import CommitProcessor
from src.utils import is_github_url, extract_github_repo
from src.visualiser import plot_line_graph, plot_bar_chart, plot_pie_chart
from src.cache import load_cached_data, save_to_cache

app = Flask(__name__)
app.secret_key = 'flaskapp_secret_key'
load_dotenv()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form.get('repo_input')
        token = os.getenv("GITHUB_API_KEY")

        try:
            if is_github_url(user_input):
                repo_type = "gh"
                identifier = extract_github_repo(user_input) if user_input.startswith("http") else user_input
                if not token:
                    flash("GitHub token not found in .env (GITHUB_API_KEY).", "error")
                    return redirect(url_for('index'))
                parser = GitHubRepoParser(identifier, token)
            else:
                repo_type = "local"
                identifier = os.path.abspath(user_input)
                parser = LocalGitParser(identifier)

            raw_commits = load_cached_data(repo_type, identifier) or parser.get_raw_commit_data()
            if not raw_commits:
                flash("Failed to retrieve commit data.", "error")
                return redirect(url_for('index'))
            else:
                save_to_cache(repo_type, identifier, raw_commits)

            processor = CommitProcessor(raw_commits)
            daily = processor.commits_per_day()
            weekly = processor.commits_per_week()
            contributors = dict(processor.top_contributors())
            top_files = dict(processor.most_edited_files())

            chart_filenames = [
                plot_line_graph(daily, "Commits Per Day", "Date", "Commits"),
                plot_line_graph(weekly, "Commits Per Week", "Week", "Commits"),
                plot_bar_chart(top_files, "Top Edited Files", "File", "Edits"),
                plot_pie_chart(contributors, "Top Contributors"),
            ]
            chart_paths = [name for name in chart_filenames]

            return render_template("results.html", charts=chart_paths)

        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            return redirect(url_for("index"))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)