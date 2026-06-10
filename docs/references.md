# References

These are the sources I used to define what a good user story is, how to clean messy data, and how to think about data quality in this project.

## 1. Mike Cohn. Mountain Goat Software. User Stories.

This is the practitioner reference for what an agile user story is.

- URL: https://www.mountaingoatsoftware.com/agile/user-stories
- Author: Mike Cohn

What I take from it:

- The classic template: *"As a <type of user>, I want <some goal> so that <some reason>."*
- The three Cs by Ron Jeffries (2001): Card (the short text), Conversation (the team discussion around it), Confirmation (the acceptance test that decides when the story is done).
- Conditions of Satisfaction. A short list of checks that has to be true for the story to be accepted. This is also called acceptance criteria.
- INVEST. A checklist for a good story: Independent, Negotiable, Valuable, Estimatable, Small, Testable.

I use this as the practical definition of a "good" user story in this project.

## 2. Lucassen, Dalpiaz, van der Werf, Brinkkemper (2016). Quality User Story (QUS) framework.

A peer reviewed academic framework with 13 quality criteria for user stories. The paper evaluated 1,023 user stories from 18 organizations and built a tool called AQUSA to detect quality defects.

- Title: *Improving agile requirements: the Quality User Story framework and tool*
- Authors: Garm Lucassen, Fabiano Dalpiaz, Jan Martijn E. M. van der Werf, Sjaak Brinkkemper
- Journal: Requirements Engineering, vol. 21, pp. 383 to 403 (2016)
- DOI: https://doi.org/10.1007/s00766-016-0250-x
- License: Open Access (CC BY 4.0)

How the 13 QUS criteria map to this project:

| QUS criterion | Category | Used in this project for |
|---|---|---|
| Well formed | Syntax | Detecting missing role or means in a story |
| Atomic | Syntax | Detecting stories that contain more than one feature |
| Minimal | Syntax | Detecting noise in the story text |
| Conceptually sound | Semantic | Validating that means and ends fit together |
| Problem oriented | Semantic | Catching implementation hints inside a story |
| Unambiguous | Semantic | Clarity scoring |
| Full sentence | Syntax | Clarity scoring |
| Estimatable | Pragmatic | Scope risk scoring |
| Unique | Pragmatic (set) | Duplicate detection |
| Uniform | Pragmatic (set) | Format consistency across the backlog |
| Independent | Pragmatic (set) | Dependency detection |
| Complete | Pragmatic (set) | Coverage gap detection |
| Conflict free | Pragmatic (set) | Conflict detection between stories |

QUS is the academic foundation for the quality dimensions I will use in notebook 04 (quality framework).

The same paper introduces AQUSA, a tool that uses natural language processing to detect QUS violations. Natural language processing (NLP) is the set of computer techniques for working with human language. AQUSA reaches 93.8 percent recall on the syntactic criteria. Recall is the share of true defects the tool catches. The tool cannot handle the semantic criteria reliably without deeper language understanding. That gap is the reason I plan to use modern large language models (LLMs) in notebook 06. An LLM is a neural network trained on huge amounts of text, like GPT.

## 3. Hadley Wickham (2016). Tidy Data.

The foundational reference for the data wrangling approach I use in notebook 02.

- Title: *ggplot2. Elegant Graphics for Data Analysis*, Chapter 9 "Data Analysis"
- Author: Hadley Wickham
- Publisher: Springer (Use R! series), 2016
- DOI: https://doi.org/10.1007/978-3-319-24277-4_9
- Original tidy data paper: Wickham, H. (2014). *Tidy data*. Journal of Statistical Software, 59(10).

Principles I apply:

1. Variables go in columns, observations go in rows. The cleaned file `data/processed/02_user_stories_clean.csv` follows this strictly. One story per row, one attribute per column.
2. One dataset per file. The cleaning notebook outputs a single canonical file rather than splitting the data across many files.
3. Tidying is a precondition for analysis, not part of it. This is why cleaning lives in its own notebook (02) separate from feature engineering (03) and scoring (05).
4. Missing values stay explicit. I do not silently fill or impute missing values. Imputation means replacing a missing value with a guess. Missingness is itself a quality signal in this project (see decision D5).

The separation between cleaning and analysis follows Wickham's recommended workflow and keeps each notebook auditable.

## 4. Thong Sze Yee, Mohd Zain, Tan (2017). Data capture-ability versus data analyzability.

A conceptual framing for why cleaning matters at all.

- Title: *An Engineering Approach to Increase Chances of Data Capture-ability and Data Analyzability in Work Measurement Practices*
- Authors: Thong Sze Yee, Zuraidah Bt. Mohd Zain, Tan Chan Sin
- Proceedings of the 2017 International Conference on Industrial Engineering and Operations Management (IEOM), Bristol, UK
- URL: https://www.ieomsociety.org/ieomuk/papers/45.pdf

The paper distinguishes between two ideas:

- Captured data. The record exists in storage.
- Analyzable data. The record can actually be used to compute a measurement.

A record can be one without being the other.

In this project, the TAWOS dataset is fully captured. Every story is in the database. But a large share is not directly analyzable because of text artifacts, missing fields, and extreme outliers. Notebook 02 (cleaning) and notebook 03 (feature engineering) exist to move records from "captured but not analyzable" into "captured and analyzable", without dropping any of them.

I cite this framing once in the case study. It is not the methodological backbone. The backbone is Wickham's tidy data principles and the QUS framework.

## How these sources connect to the notebooks

| Notebook | Sources used |
|---|---|
| 01 Data Understanding | Cohn (template detection), Lucassen (QUS Well formed), Wickham (tidy data layout) |
| 02 Data Cleaning | Wickham (tidy data, keep missing explicit), Thong (capture vs analyze framing) |
| 03 Feature Engineering | Lucassen (QUS criteria become features) |
| 04 Quality Framework | Lucassen (the 13 criteria define the score dimensions), Cohn (INVEST checks) |
| 05 Rule based Scoring | Lucassen (AQUSA style rules), Cohn (Conditions of Satisfaction) |
| 06 AI Scoring | Lucassen (LLM prompts grounded in QUS), Cohn (template grounding) |