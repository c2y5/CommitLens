from flask import Flask, render_template, request, redirect, url_for, flash, Response, stream_with_context, jsonify
import os
from dotenv import load_dotenv
import glob

from src.parser import LocalGitParser
from src.github_parser import GitHubRepoParser
from src.processing import CommitProcessor
from src.utils import is_github_url, extract_github_repo
from src.visualiser import plot_line_graph, plot_bar_chart, plot_pie_chart
from src.cache import delete_cache, save_to_cache

app = Flask(__name__)
app.secret_key = 'flaskapp_secret_key'
load_dotenv()

GITHUB_TOKENS = os.getenv("GITHUB_API_KEY", "").split(",")
GITHUB_TOKENS = [t.strip() for t in GITHUB_TOKENS if t.strip()]

generated_charts = []

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route("/cache/invalidate", methods=["POST"])
def invalidate_cache():
    data = request.get_json()
    repo_input = data.get("repo_input")

    if not repo_input:
        return jsonify({"status": "error", "message": "Missing repo_input"}), 400

    try:
        if is_github_url(repo_input):
            repo_type = "gh"
            identifier = extract_github_repo(repo_input) if repo_input.startswith("http") else repo_input
        else:
            repo_type = "local"
            identifier = os.path.abspath(repo_input)

        success = delete_cache(repo_type, identifier)
        if success:
            return jsonify({"status": "success", "message": "Cache invalidated"})
        else:
            return jsonify({"status": "error", "message": "No cache found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/progress", methods=["POST"])
def progress():
    user_input = request.form.get("repo_input")

    @stream_with_context
    def stream_generator():
        global generated_charts
        try:
            if not user_input:
                yield "No repository input provided.\n"
                return

            if is_github_url(user_input):
                repo_type = "gh"
                identifier = extract_github_repo(user_input) if user_input.startswith("http") else user_input
                if not GITHUB_TOKENS:
                    yield "GitHub token not found in .env (GITHUB_API_KEY)\n"
                    return
                parser = GitHubRepoParser(identifier, GITHUB_TOKENS)
            else:
                repo_type = "local"
                identifier = os.path.abspath(user_input)
                parser = LocalGitParser(identifier)

            yield from parser.get_raw_commit_data_yielding()

            raw_commits = parser.get_raw_commit_data()
            if not raw_commits:
                yield "Failed to retrieve commit data.\n"
                return

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

            generated_charts = chart_filenames

            yield "__COMPLETE__\n"

        except Exception as e:
            yield f"Error: {str(e)}\n"

    return Response(stream_generator(), mimetype="text/plain") # type: ignore

@app.route("/results")
def results():
    if not generated_charts:
        flash("No analysis results available.", "error")
        return redirect(url_for("index"))

    return render_template("results.html", charts=generated_charts)

if __name__ == "__main__":
    for file in glob.glob(os.path.join("static", "*.html")):
        try:
            os.remove(file)
        except Exception as e:
            print(f"Failed to delete {file}: {e}")

    app.run(debug=True, host="0.0.0.0", port=5000)
