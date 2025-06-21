# CommitLens 🔎

CommitLens is a Python tool to visualize Git commit data from **local repositories** or **GitHub repositories**. It generates interactive charts displaying commit activity, contributor statistics, and file modification patterns, helping developers analyze project history easily.

[Try it out yourself here!](https://commitlens.iamsky.hackclub.app)

---

![Banner](./img/CommitLensBanner.jpg)

---

## Features 🔥

- Supports **local Git repositories** and **GitHub repositories** via API.
- Visualizes:
  - Commits per day and week (line charts)
  - Top contributors (pie chart)
  - Most edited files (bar chart)
- Cache system with 4-hour expiration to reduce redundant API calls or local Git parsing.
- Respects `.gitignore` rules to ignore unwanted files from analysis.
- Web UI for better visual

---

## Installation 📦

1. Clone the repo:
    ```bash
   git clone https://github.com/c2y5/CommitLens.git
   cd CommitLens
    ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` and rename to `.env` with your GitHub API token(s):

   ```
   GITHUB_API_KEY=token1,token2
   ```

---

## Usage 🚀


```bash
python app.py
```
Then go to ``localhost:5000``

---

## Project Structure 📂

```
CommitLens/
├── cache/
│   └── data.json                # Cache file for all repos
├── src/
│   ├── parser.py                # Local Git repository parser
│   ├── github_parser.py         # GitHub API repository parser
│   ├── processing.py            # Data processing logic
│   ├── visualizer.py            # Creating charts with plotly
│   ├── cache.py                 # Cache handling
│   └── utils.py                 # Helper functions
├── static/
│   └── style.css                # Website style
├── templates/
│   ├── index.html               # Homepage of the website
│   └── results.html             # Result page of the website
├── main.py                      # Main script to run the tool
├── requirements.txt             # Python dependencies
├── setup.sh                     # Initialise the project env
└── .env.example                 # Environment variables
```

---

## Dependencies 🔨

Git
Python 3.10+
* `GitPython`
* `requests`
* `python-dotenv`
* `pathspec`
* `flask`
* `plotly`
* `Pandas`
* `gunicorn`

---

## License 📄

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---

## Contributing 🤝

Contributions and suggestions are welcome! Please open issues or submit pull requests.

---