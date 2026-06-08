# AI-Supported Requirement Quality Analytics Dashboard

A portfolio project that looks at the quality of user stories in Agile teams using data analysis and AI.

The goal is: figure out which user stories are clear, complete, and ready for development, and which ones are not. Show the results in a dashboard.

Work in progress.

---

## What this project does

User stories in Agile projects are not always written well. Sometimes a story is missing a description, has no acceptance criteria, or doesn't say who the user is. This causes rework, confusion between teams, and slow sprints.

This project tries to make these problems visible by:

- scoring each story across a few quality dimensions (clarity, completeness, testability, business value, scope risk)
- combining rule-based scoring with an AI assisted review
- showing the results in a Power BI dashboard and a small Streamlit app

## Who it is for

- Product Owners and Business Analysts who want to see if stories are ready
- QA people who care about testability
- Scrum Masters who want to spot risky items before sprint planning

## Tools used

- Python (pandas, numpy)
- Jupyter Notebook
- MySQL 8.0
- SQLAlchemy + pymysql
- Plotly + Streamlit
- Power BI
- OpenAI API (planned)

## Folder structure
data/ raw, interim, processed data (raw not committed)
notebooks/ Jupyter notebooks, numbered by step
src/ reusable Python code
sql/ SQL queries and schema
dashboards/ Power BI and Streamlit files
docs/ findings and decisions

## Data

I am using the TAWOS dataset (version 1.1) — about 458,000 issues from 39 open-source projects, originally mined from public Jira repositories.

Citation:
Tawosi, V., Al-Subaihin, A., Moussa, R., & Sarro, F. (2022). *A Versatile Dataset of Agile Open Source Software Projects.* MSR 2022.
DOI: https://doi.org/10.5522/04/21308124
License: Apache 2.0.

For this project I only use the issues with `Type = 'Story'` — that gives about 31,000 user stories to work with.

More detail in docs/findings.md.
