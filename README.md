# CommitLens 🔎

CommitLens is a Python tool to visualise Git commit data from **local repositories** or **GitHub repositories**. It generates interactive charts displaying commit activity, contributor statistics, and file modification patterns, helping developers analyse project history easily.

[Try it out yourself here!](https://commitlens.iamsky.hackclub.app)

---

![Banner](./img/CommitLensBanner.jpg)

---

## Features 🔥

- Supports **local Git repositories** and **GitHub repositories** via API.
- Visualises:
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

3. Copy `.env.example` and rename to `.env` with your GitHub API token:

   ```
   GITHUB_API_KEY=your_personal_access_token_here
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
│   ├── visualiser.py            # Chart plotting functions using matplotlib
│   ├── cache.py                 # Cache handling
│   └── utils.py                 # Helper functions
├── static/
│   └── style.css
├── templates/
│   ├── index.html
│   └── results.html
├── main.py                      # Main script to run the tool
├── requirements.txt             # Python dependencies
└── .env.example                 # Environment variables
```

---

## Dependencies 🔨

* Python 3.10+
* `GitPython`
* `requests`
* `pathspec`
* `python-dotenv`
* `Flask`
* `plotly`

---

## License 📄

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---

## Contributing 🤝

Contributions and suggestions are welcome! Please open issues or submit pull requests.

---