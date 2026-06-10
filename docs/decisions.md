# Analysis Decisions Log

This file tracks the choices I made while working on this project. For each choice it lists the options I considered and why I picked one. I write decisions down so I can explain them later in the case study and so a reviewer can audit my reasoning.

## D1. Dataset choice: TAWOS instead of the raw Zenodo dump

Options I considered:
- The raw Zenodo Public Jira Dataset. It is about 6.3 TB and ships as a MongoDB dump. MongoDB is a NoSQL database that stores data as JSON like documents. Access is restricted.
- TAWOS version 1.1. It is about 4 GB and ships as a MySQL dump. MySQL is a standard relational database. Apache 2.0 license, public.

My choice: TAWOS.

Reason: TAWOS is the cleaned, structured version of the same Jira projects. I can download it without applying for access, it has documentation, and the size fits a portfolio project (about 458,000 issues, 4 GB). The raw Zenodo dump would force me to install MongoDB, ask for permission, and use storage I do not need.

Source for the dataset: Tawosi et al. (2022), see `docs/references.md`.

## D2. Storage: MySQL over SQLite or flat files

My choice: MySQL 8.0.

Reason: TAWOS already ships as a MySQL `.sql` file. A dump is a text export of all tables. Importing this file directly into MySQL avoids any conversion step. It also matches the project plan, which says step 7 is to use a SQL database. Later on Power BI can connect to MySQL with no extra work.

## D3. Filter strategy: only `Type = 'Story'`

Options I considered:
- (A) Strict. Keep only rows where the Jira type is `Story`. This gives 31,394 rows.
- (B) Broader. Story plus New Feature plus Enhancement Request.
- (C) Even broader. Add Improvement too.

My choice: A.

Reason: The project is about the quality of user stories, not the quality of any backlog item. Mixing types would water down the analysis. I can always come back later and add more types if I need more data.

## D4. Keep Lsstcorp even though it dominates

One project, Lsstcorp Data Management, contributes 62 percent of all stories.

Options I considered:
- Keep all rows and let the dashboard filter by project.
- Cap Lsstcorp at 5,000 rows so it does not dominate.
- Remove Lsstcorp entirely.

My choice: Keeping all rows.

Reason: Dropping data is destructive. Capping introduces sampling bias. The smaller sample no longer represents the project. Letting the user toggle Lsstcorp on and off in the dashboard is the honest option. The user can see both views and judge the impact.

## D5. Keep stories with missing description

About 4,067 stories have no description at all.

My choice: Keep them in the dataset.

Reason: A missing description is itself a sign of poor quality. If I drop these rows I am erasing the exact low quality records I want to measure. They will get a low quality score and they will contribute to a `missing_description` issue tag.

## D6. Drop the Priority field from scoring

The Priority column is empty in 62 percent of stories.

My choice: Exclude Priority from the quality framework.

Reason: There is not enough signal. A column with so many missing values adds noise instead of information.

## D7. Native MySQL for now, Docker later

Options I considered:
- Native MySQL install on Windows. Quick to set up, MySQL Workbench (a graphical client) works out of the box.
- Docker Compose. A way to describe a service in a small file and run it in an isolated container. Containers are like lightweight virtual machines. More portable, harder to set up the first time on Windows.

My choice: Native MySQL for the current phase. Add Docker Compose later, after the main work is done.

Reason: The point of this project is the data analytics work, not the infrastructure. The native install gets me to the data faster. Once the cleaning, scoring, and dashboards are in place I will add a `docker-compose.yml` so anyone can reproduce the setup with one command.