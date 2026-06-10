# AI-Supported Requirement Quality Analytics Dashboard

A portfolio project that looks at the quality of user stories in agile teams using data analysis and AI.

The goal is to figure out which user stories are clear, complete, and ready for development, and which ones are not. Then show the results in a dashboard.

Work in progress.

## What this project does

User stories in agile projects are not always written well. Sometimes a story is missing a description, has no acceptance criteria (a checklist of what makes the story done), or does not say who the user is. This causes rework, confusion between teams, and slow sprints.

This project tries to make these problems visible by:

- Scoring each story across a few quality dimensions. Clarity, completeness, testability, business value, scope risk.
- Combining rule based scoring with an AI assisted review.
- Showing the results in a Power BI dashboard and a small Streamlit app. Streamlit is a Python library for quickly building data web apps.

## Who it is for

- Product Owners and Business Analysts who want to see if stories are ready for the next sprint.
- QA people who care about whether a story can actually be tested.
- Scrum Masters who want to spot risky items before sprint planning.

## Tools used

- Python (pandas, numpy). For data work.
- Jupyter Notebook. For step by step analysis I can show to a reader.
- MySQL 8.0. For relational storage.
- SQLAlchemy plus pymysql. For talking to MySQL from Python.
- Plotly plus Streamlit. For interactive visuals and a small web app.
- Power BI. For the business focused dashboard.
- OpenAI API. Planned, for the AI assisted scoring step.

## Folder structure

```
data/         raw, interim, processed data (raw is not committed)
notebooks/    Jupyter notebooks, numbered by step
src/          reusable Python code
sql/          SQL queries and schema
dashboards/   Power BI and Streamlit files
docs/         findings, decisions, references
```

## Data

I use the TAWOS dataset, version 1.1. It contains about 458,000 issues from 39 open source projects, originally mined from public Jira repositories.

Citation:
Tawosi, V., Al-Subaihin, A., Moussa, R., & Sarro, F. (2022). *A Versatile Dataset of Agile Open Source Software Projects.* MSR 2022.
DOI: https://doi.org/10.5522/04/21308124
License: Apache 2.0

For this project I only use issues where `Type = 'Story'`. That gives about 31,000 user stories to work with.

## How to run it locally

1. Clone the repo.
2. Install Miniconda (a small Python environment manager) and MySQL Community Server 8.0.
3. Set up the Python environment:
   ```bash
   conda create -n rqad python=3.11 -y
   conda activate rqad
   pip install -r requirements.txt
   ```
4. Download the TAWOS dump from the DOI link above. Import the `.sql` file into a MySQL database called `TAWOS`.
5. Create a `.env` file in the project root with your MySQL credentials:
   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=your-password
   DB_NAME=TAWOS
   ```
6. Open the notebooks in VS Code and pick the `rqad` kernel.

## Progress

- [x] Project setup and folder structure
- [x] TAWOS dataset imported into MySQL
- [x] First look at the data, notebook 01 (see `docs/findings.md`)
- [x] Data cleaning, notebook 02
- [ ] Feature engineering, notebook 03
- [ ] Quality scoring rules, notebook 04 and 05
- [ ] AI assisted scoring, notebook 06
- [ ] Power BI dashboard
- [ ] Streamlit app
- [ ] Final write up

## A few things I noticed so far

- Only about 7 percent of issues in this dataset are typed as `Story`. Most are bugs.
- About 13 percent of user stories have no description at all.
- About 31 percent have no Story Point estimate. About a third of those that have one use non Fibonacci values.
- Less than 1 percent of stories follow the classic *"As a [user], I want [feature], so that [reason]"* template from Mike Cohn.
- One project (Lsstcorp) is 62 percent of all stories. The dashboard will let users filter it out.
- 540 stories are exact duplicates within the same project. In one case, the same Spring XD story was filed four times within three minutes.

More detail in `docs/findings.md`. The sources behind the quality framework are in `docs/references.md`. My analysis choices are in `docs/decisions.md`.

## License

MIT for the code in this repo. The TAWOS dataset keeps its Apache 2.0 license.