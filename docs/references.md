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

## 5. Yamani, Baslyman, Ahmed (2025). UStAI dataset, LLMs for user story generation.

A recent empirical study that uses large language models to generate user stories and evaluates them with the QUS framework.

- Title: *Leveraging LLMs for User Stories in AI Systems: UStAI Dataset*
- Authors: Asma Yamani, Malak Baslyman, Moataz Ahmed
- Conference: 21st International Conference on Predictive Models and Data Analytics in Software Engineering (PROMISE), Trondheim, Norway, 2025
- DOI: https://doi.org/10.1145/3727582.3728689
- Dataset: https://github.com/asmayamani/EthicsRequirementsData (1260 annotated user stories)

What I take from it:

- A working pipeline for using an LLM to score user stories on the 13 QUS criteria. This is the closest existing reference to what notebook 06 will do.
- A public dataset of 1260 LLM-generated user stories annotated for quality, non-functional requirements (NFR), and ethical principles. Useful as a comparison point for the LLM-based scoring I will run on TAWOS.
- Patterns of LLM failure modes that I should expect, such as non-atomic stories (multiple features stitched with "and"), missing reasons after "as a", and vague wording.
- Confirmation that LLM-generated stories can be evaluated with QUS just like human-written ones, so the QUS framework can be applied across both human and LLM sources of user stories.

How I will use it: as a methodological reference for notebook 06 prompts, as a check on the kinds of quality issues to look for in AI-generated text, and as a comparison dataset if I want to benchmark my own scoring against an existing labeled corpus.

## 6. Zul, Yasin, Sahid (2025). Systematic literature review of user story quality frameworks.

A systematic literature review that compares the frameworks used by other studies to evaluate user story quality.

- Title: *User Story Quality Evaluation: Analyzing Frameworks and Application Methods*
- Authors: Muhammad Ihsan Zul, Suhaila Mohd. Yasin, Dadang Syarif Sihabudin Sahid
- Journal: ASEAN Engineering Journal, vol. 15, no. 4 (2025), pp. 115 to 123
- DOI: https://doi.org/10.11113/aej.V15.24306

Key findings I rely on:

- Of the 26 studies reviewed, INVEST is the most used framework (11 studies) and QUS is the second most used (10 studies). This justifies my choice of these two frameworks as the backbone of notebook 04.
- The authors extract 8 criteria that appear across multiple frameworks: Independent, Unambiguous, Complete, Estimable, Testable, Conflict free, Atomic, Negotiable. I will treat these as a minimum core set in the scoring framework.
- AQUSA, the QUS-based tool from Lucassen et al. (2016), is still the most common automated tool five years later. This supports the decision to keep my rule-based scoring (notebook 05) aligned with AQUSA-style checks.
- The review reports that generative AI is starting to appear in this space but is used in only one of the 26 studies. The Yamani et al. (2025) paper above is a recent example. This positions my notebook 06 in an active, under-explored area.

How I will use it: as the literature-review backbone of the case study, to show that the framework choices (QUS plus INVEST) and the tooling choices (rule-based plus LLM-based) are consistent with the current state of the field.

## 7. Mordal et al. (2012). Squale model for software quality metrics aggregation.

The methodological backbone for the scoring framework in this project. Squale is a model that has been used in real industrial settings at Air France-KLM and Peugeot-Citroen since 2010.

- Title: *Software quality metrics aggregation in industry*
- Authors: Karine Mordal, Nicolas Anquetil, Jannik Laval, Alexander Serebrenik, Bogdan Vasilescu, Stéphane Ducasse
- Journal: Journal of Software: Evolution and Process, vol. 25, issue 10, pp. 1117 to 1135 (October 2013)
- DOI: https://doi.org/10.1002/smr.1558

What I take from it:

- The clear separation between composition (combining different metrics into a single quality interval) and aggregation (summarizing component-level results to system level). Notebook 03 did composition. Notebook 04 will do aggregation.
- The argument that simple arithmetic mean hides bad components, with concrete industrial examples. This is exactly why I will not use plain averages in scoring.
- The hard, medium, soft weighting scheme using lambda equals 30, 9, 3. This gives me a parameterised way to make the score more or less sensitive to bad components.
- The aggregation function ISquale(x1, ..., xn) = minus log base lambda of the mean of lambda to the minus xi. It is proven to never give a result worse than the smallest input and never better than the arithmetic mean.
- The "anti transfers principle" which guarantees that any improvement in component quality is reflected in the aggregated score. Plain averages and several econometric indices do not satisfy this.
- A list of nine requirements that a good quality aggregation method should satisfy. I will use these as a checklist when designing my own scoring framework.

How I will use it: as the direct reference for the aggregation step in notebook 05. The lambda based weighted average will be applied when combining per-story scores into per-project and overall scores.

## 8. Challa et al. (2011). Fuzzy multi-criteria approach to integrated software quality evaluation.

A reference for the multi-perspective scoring structure and the interpretation bands.

- Title: *Integrated Software Quality Evaluation: A Fuzzy Multi-Criteria Approach*
- Authors: Jagat Sesh Challa, Arindam Paul, Yogesh Dada, Venkatesh Nerella, Praveen Ranjan Srivastava, Ajit Pratap Singh
- Journal: Journal of Information Processing Systems, vol. 7, no. 3 (September 2011), pp. 473 to 518
- DOI: https://doi.org/10.3745/JIPS.2011.7.3.473

What I take from it:

- The idea of evaluating software quality from three perspectives: developer, user, and project manager. In this project I map these onto the dashboard audiences: Product Owner / Business Analyst, QA, and Scrum Master / Project Manager.
- A four level hierarchical structure: metrics, then sub characteristics, then characteristics, then perspectives, then overall. This is the same pattern that Squale uses and that I follow in notebook 04.
- An interpretation table for the final score, which I will adapt to a zero to five scale:
  - Very Good: greater than 0.65 of the maximum
  - Good: 0.5 to 0.65
  - Average: 0.35 to 0.5
  - Poor: 0.25 to 0.35
  - Very Poor: less than 0.25
- The use of weighted averages at each level. Combined with the Squale lambda weighting, this gives the scoring its sensitivity to bad components.

How I will use it: as a reference for the score interpretation bands in the dashboard and the case study, and to justify the three perspective split in the Power BI dashboard.

## Optional further reading (not directly used in this project)

- Yan et al. (2017). *Automating Aggregation for Software Quality Modeling*. IEEE ICSME 2017. DOI: https://doi.org/10.1109/ICSME.2017.30. This paper uses a topic model (DPLSA) to learn aggregation weights from a benchmark of open source projects, removing the need for manual weights. It is more research oriented than the practical Squale approach and is left for future work in this project.

## 9. Hashemi, Eisner, Rosset, Van Durme, Kedzie (2024). LLM-RUBRIC: A Multidimensional, Calibrated Approach to Automated Evaluation of Natural Language Texts.

The methodological backbone for the AI-supported scoring in notebook 06.

- Title: *LLM-RUBRIC: A Multidimensional, Calibrated Approach to Automated Evaluation of Natural Language Texts*
- Authors: Helia Hashemi, Jason Eisner, Corby Rosset, Benjamin Van Durme, Chris Kedzie (Microsoft)
- Venue: Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (ACL 2024), pp. 13806 to 13834
- DOI: https://aclanthology.org/2024.acl-long.745

What I take from it:

- The argument that naive LLM scoring is unreliable even though the LLM is highly capable. They show that a single LLM-as-judge correlates poorly with human judges, but combining the LLM's distribution over multiple rubric questions (calibrated against humans) gives strong correlation.
- The use of a multi-dimensional rubric covering different evaluation criteria. This matches my 5-dimension framework in notebook 04 (clarity, completeness, testability, business value, scope risk).
- The principle of asking each rubric question independently of the others, to avoid the LLM confounding its own responses. I will follow this in notebook 06.
- Validation that 9 rubric questions can predict overall quality with RMSE less than 0.5 on a 1 to 4 scale, a 2x improvement over the uncalibrated baseline.

How I will use it: as a justification for asking the LLM multiple specific questions per story (one per dimension or one per criterion) rather than a single "rate this story 1 to 5" question. This is the same multi-question approach I already used for rule-based scoring in notebook 05.

## 10. Croxford et al. (2025). Automating Evaluation of AI Text Generation in Healthcare with LLM-as-a-Judge.

The most direct precedent for what I will do in notebook 06: use a strong LLM to score multi-document summaries against a multi-attribute rubric, then validate against human judges.

- Title: *Automating Evaluation of AI Text Generation in Healthcare with a Large Language Model (LLM)-as-a-Judge*
- Authors: Emma Croxford, Yanjun Gao, Elliot First, Nicholas Pellegrino, Miranda Schnier, John Caskey, Madeline Oguss, Graham Wills, Guanhua Chen, Dmitriy Dligach, Matthew Churpek, Anoop Mayampurath, Frank Liao, Cherodeep Goswami, Karen Wong, Brian Patterson, Majid Afshar
- Venue: medRxiv preprint, 2025
- DOI: https://doi.org/10.1101/2025.04.22.25326219

What I take from it:

- They benchmark 8 LLMs as judges for clinical summary evaluation using the PDSQI-9 rubric (a 9-attribute scoring instrument similar in spirit to QUS).
- Key result: GPT-o3-mini with 5-shot prompting achieved the highest intraclass correlation coefficient with human judges (ICC equal to 0.818). It completed each evaluation in about 22 seconds.
- Reasoning models (GPT-o3-mini, DeepSeek R1) outperformed non-reasoning models (GPT-4o, Mixtral 8x22B) on evaluations that require advanced reasoning and domain expertise. This is relevant to my Cohn template and INVEST checks which require some reasoning.
- Multi-agent frameworks did not consistently outperform a well-prompted single LLM judge, while costing more. I will start with single LLM judges in notebook 06.
- Inter-rater reliability is the standard outcome metric: intraclass correlation coefficient (ICC), Krippendorff's alpha, Gwet's AC2. I will use these to compare my AI-supported scores to my rule-based scores from notebook 05.
- Few-shot prompting (5 examples) and structured JSON output produced the most reliable results.

How I will use it: as the direct template for the notebook 06 design. I will start with a single LLM judge using 5-shot prompting and structured JSON output, score a sample of my 31,394 stories, and report ICC and correlations against my rule-based scores from notebook 05.

## 11. van Schaik and Pugh (2024). A Field Guide to Automatic Evaluation of LLM-Generated Summaries.

Industry-oriented practical guidance for automatic evaluation, used as the sanity check framework for my evaluation suite.

- Title: *A Field Guide to Automatic Evaluation of LLM-Generated Summaries*
- Authors: Tempest van Schaik, Brittany Pugh (Microsoft)
- Venue: Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR 2024)
- DOI: https://doi.org/10.1145/3626772.3661346

What I take from it:

- The principle of using a suite of metrics rather than a single metric. Each metric has weaknesses. I use rule-based scores (notebook 05) and will add AI-supported scores (notebook 06) as complementary signals.
- The combination of standard metrics (ICC, correlation) with custom metrics designed for the specific task. My 5 quality dimensions are custom metrics in this sense.
- The combination of LLM and non-LLM metrics. My rule-based scoring is non-LLM, while notebook 06 will add an LLM evaluator. Discrepancies between the two are themselves a useful signal.
- The need to validate any custom evaluator. I will validate notebook 06's LLM scores by checking their correlation with notebook 05's rule-based scores on the same stories, and by spot checking the LLM's reasoning on hand-picked examples.
- The cold start problem and the suggestion to use synthetic data carefully or repurpose existing datasets. In my case, the dataset is real Jira data, so this is less of a concern.
- The challenge of distinguishing good from excellent. LLMs can saturate at the top of the scale. Using both rule-based and LLM-based scores together, and using multiple dimensions, helps mitigate this.

How I will use it: as a checklist for the design of notebook 06. I will produce a suite of LLM scores (not just one), combine them with the rule-based scores from notebook 05, validate them against each other, and report disagreements as a signal worth investigating.