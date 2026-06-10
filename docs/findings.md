# Findings and Insights

This file collects the insights I found while exploring and cleaning the data. Each finding is something I can point to later in the case study. I write findings down so I do not lose them between sessions.

The sources I refer to (Cohn, Lucassen, Wickham, Thong) are listed in full in `docs/references.md`.

## Notebook 01. Data Understanding

**Date:** Session 1. Data understanding phase.
**Dataset:** TAWOS v1.1. 458,232 issues from 39 open source projects.
**Working subset:** 31,394 issues filtered to `Type = 'Story'`.

### Finding 1. Most issues in the dataset are bugs, not stories

Bug type issues make up 47 percent of the dataset (215,570 out of 458,232). Only 6.85 percent are typed as `Story` (31,394 issues).

Business meaning: even in well known open source projects, writing real user stories is the minority practice. This makes the case for paying attention to backlog item quality.

### Finding 2. One project dominates the story pool

Lsstcorp Data Management contributes 19,578 stories, which is 62 percent of all Story type issues. The other 21 projects share the remaining 11,816 stories.

Risk: any insight that averages across projects will be heavily biased by Lsstcorp.

What I did about it: I kept all stories in the dataset and exposed `Project_Name` as a dashboard filter. See decision D4.

### Finding 3. Missing description is a real quality issue

13 percent of user stories (about 4,067) have no description and no Description_Text at all. They ship with just a title.

This itself is a quality signal, not a data problem. Stories without a description will get a `missing_description` issue tag in the scoring framework.

### Finding 4. Story Point coverage is uneven

31 percent of stories (9,661) have no Story Point estimate. A Story Point is a relative effort number that agile teams give to a backlog item. Where the value is present the distribution looks healthy. The median is 3 and the 75th percentile is 5, which is in line with Fibonacci numbers used in Planning Poker. Planning Poker is a planning game where the team estimates effort with a fixed scale.

Outlier alert: one story has a Story Point value of 105. An outlier is a value far away from the rest of the distribution. A value this high makes no sense as a single backlog item.

Also, 13 percent of stories had their Story Point value changed after the first estimate. Estimates that change a lot are a sign that the team did not understand the story when they first sized it.

### Finding 5. The Priority field is mostly empty

62 percent of stories (19,582) have no Priority value. The Priority field carries no useful signal for this analysis. See decision D6.

### Finding 6. The text has artifacts that need cleaning

While inspecting the raw rows I saw:

- Titles wrapped in double quotes, for example `"Fix stream failover "`.
- Description_Text fields prefixed with three double quotes, for example `"""See https://..."`.
- Trailing whitespace inside the quoted titles.

Action: clean these in notebook 02 using regex. Regex is a small language for matching text patterns.

### Finding 7. Resolution time covers an extreme range

Resolution time is how long the team took to close the story. The median is about 14 days, which is a normal sprint length. The maximum is about 8 years (4.3 million minutes). The 25th percentile is about 6 hours, which is way too short for a real user story and looks more like a bug fix.

Open question: are the very fast resolutions actually user stories, or are they mislabeled bug fixes?

### Finding 8. The data covers 11 years

The dataset spans from August 2009 to October 2020. That is enough history to track quality trends over time.

### Finding 9. Less than 1 percent of stories follow the classic user story template

The classic template comes from Mike Cohn (Mountain Goat Software): *"As a <type of user>, I want <some goal> so that <some reason>."* The QUS framework by Lucassen et al. (2016) calls the same idea "Well formed".

I used regex to detect the role marker ("as a" or "as an"), the means marker ("I want", "I need", "I would like", and variants), and the reason marker ("so that"). Results on 31,394 stories:

| Pattern check | Stories | Share |
|---|---:|---:|
| Has any description (non empty) | 27,327 | 87.0% |
| Has "as a" or "as an" (role marker) | 2,390 | 7.6% |
| Has "I want / need / would like" (means marker) | about 3,800 | about 12% |
| Has "so that" (reason marker) | 1,235 | 3.9% |
| QUS Well formed (role plus means) | 871 | 2.8% |
| Full Cohn template (role plus means plus reason) | 284 | 0.9% |

Interpretation: even in mature open source projects where the team labeled the item as User Story on purpose, the classic agile template is almost never used in the description.

Business impact: without an explicit role, want, and reason, readers (developers, QA, business analysts) have to guess who the user is and why the feature matters. That is exactly the kind of confusion that causes sprint rework.

Caveat I checked: maybe teams write the template in the Title instead of the Description. Result of the check: only 2.4 percent of titles contain "as a", 2.1 percent contain "I want", and 0.2 percent contain "so that". Combining Title and Description, only 321 stories (1.0 percent) contain the full template anywhere. The conclusion holds.

### Finding 10. Story Point values are not consistently Fibonacci

Planning Poker uses a modified Fibonacci scale: 1, 2, 3, 5, 8, 13, 21, 34, 55, 89. Teams that follow the scale rarely give a story a value of 4, 6, 7, or 10. In this dataset:

| Value | Count | On the Fibonacci scale |
|---|---:|---|
| 1 | 4,165 | Yes |
| 2 | 3,648 | Yes |
| 3 | 2,285 | Yes |
| **4** | **2,082** | **No** |
| 5 | 1,643 | Yes |
| **6** | **1,059** | **No** |
| 8 | 1,640 | Yes |

The non Fibonacci values 4 and 6 together account for about 14 percent of all estimated stories. Some teams either skip Planning Poker or use a plain linear scale (1, 2, 3, 4, 5, 6, 7, ...). This is a sign of lower estimation maturity.

Action: a feature called `is_fibonacci_sp` will flag whether a story's estimate sits on the canonical scale. Notebook 03 will compute this.

### Finding 11. 75 stories have Story Point of 40 or more

The maximum Story Point is 105, which would be about 21 sprints of work for one story. There are 75 stories with a value of 40 or more.

Interpretation: these are not user stories in the agile sense. They are epics that were never broken down. An epic is a large piece of work that should be split into smaller stories. These rows violate the QUS criterion *Estimatable* (Lucassen et al., 2016) and the INVEST acronym *Small* (Cohn). INVEST is a checklist for a good story: Independent, Negotiable, Valuable, Estimatable, Small, Testable.

Action: notebook 02 added `flag_sp_high_scope_risk` (Story Point of 13 or more) and `flag_sp_extreme_scope_risk` (40 or more). The flags do not remove the rows. They mark them.

Visual evidence from the histogram I drew:

- Strong Fibonacci peaks at 1, 2, 3, 5, and 8. Planning Poker is the dominant practice.
- Secondary peaks at 4 and 6. About 14 percent of estimates are off scale.
- A clear dip at 7, between 6 and 8. Teams that do use Fibonacci jump from 6 to 8 directly.
- A peak at 10. This is the "round number" preference, typical of linear estimation.
- A peak at 0. Stories with zero effort should not be classified as user stories.

### Finding 12. Template adoption peaked in 2014 and 2015, then collapsed

Looking at year by year breakdown:

| Year | Total stories | Has "as a" % | Full Cohn template % | Has Story Point % |
|---|---:|---:|---:|---:|
| 2010 | 174 | 4.0% | 0.0% | 66.7% |
| 2013 | 1,893 | 8.6% | 0.3% | 69.9% |
| **2014** | **2,346** | **10.9%** | **5.0%** | 74.4% |
| **2015** | **3,676** | **17.4%** | 1.6% | 79.5% |
| 2016 | 3,734 | 4.9% | 0.2% | 75.8% |
| 2017 | 4,873 | 6.3% | 0.3% | 62.6% |
| 2020 | 3,890 | 5.2% | 0.2% | 72.9% |

The trend:

- 2009 to 2013: almost no template use. The "User Story" type is just a Jira label.
- 2014 to 2015 (the golden age): a sharp rise. Cohn template peaks at 5.0 percent, "as a" prefix peaks at 17.4 percent. This matches the period when agile methodology marketing was at its peak.
- 2016 onward: collapse. Adoption falls back to pre 2014 levels and stays there.

This is a counter intuitive finding. I expected template use to grow over time as agile spread. Instead, after 2015 it dropped and never came back.

Possible explanations to investigate in the dashboard:
1. A small set of disciplined projects dominated the early years. Later, more projects joined and diluted the average.
2. Teams kept labeling items as User Story in Jira but stopped following the format.
3. The 2014 and 2015 peak was tied to the height of agile marketing. After that, teams reverted to plain prose.

Positive trend: Story Point coverage stabilized at about 70 percent from 2013 onwards. Estimation discipline outlived template discipline.

### Finding 13. Lsstcorp explains the post 2015 collapse

Breakdown by project (only projects with at least 100 stories):

| Project | Stories | Has "as a" % | Full Cohn % | Has SP % |
|---|---:|---:|---:|---:|
| MongoDB Compass | 175 | 51.4% | 34.3% | 19.4% |
| Spring XD | 2,593 | 26.5% | 6.1% | 100.0% |
| Hyperledger Indy Node | 349 | 16.6% | 5.4% | 28.9% |
| Sonatype Nexus | 243 | 9.9% | 3.3% | 45.3% |
| DotNetNuke Platform | 402 | 34.6% | 2.7% | 73.9% |
| Hyperledger Fabric | 2,748 | 11.5% | 0.5% | 10.8% |
| **Lsstcorp Data management** | **19,578** | **4.1%** | **0.0%** | **81.3%** |
| Apache Mesos | 151 | 9.3% | 0.0% | 15.2% |

Lsstcorp, which is 62 percent of the dataset, has zero stories matching the full Cohn template. Because it dominates the dataset, it pulls the overall adoption rate from a potential 3 to 6 percent down to the observed 0.9 percent.

For the dashboard: users will be able to filter Lsstcorp out and see what the rest of the open source community looks like.

### Finding 14. Different projects fail in different ways

Looking at the project table, some projects show partial use of the template. This is useful because it points to the exact place where each team breaks down.

- DotNetNuke Platform: 34.6 percent start with "as a" but only 2.7 percent complete the template. The team declares a user role but skips the reason. This is the Business Value failure mode that the QUS criterion "Conceptually sound" (Lucassen et al., 2016) targets.
- Hyperledger Fabric: 11.5 percent have "as a" but only 10.8 percent have a Story Point. The team writes stories but does not estimate them. Backlog readiness is incomplete.
- Titanium SDK and Aptana Studio: average Story Point is around 7.3, vs the dataset median of 3. These projects routinely violate INVEST Small. They label epics as stories.
- Story Point coverage spans 21x, from 4.7 percent (Alloy Framework) to 100 percent (Spring XD). Estimation discipline is wildly inconsistent across teams.

Recommendation surface: the dashboard can produce per project advice. For example, DotNetNuke gets "enforce so that clauses". Hyperledger Fabric gets "require estimates before sprint commit". This turns the analytics into actionable feedback instead of just numbers.

## Notebook 02. Data Cleaning findings

### Finding 15. 35 stories contained only markup

After stripping Jira markup (`{code}`, `{noformat}`), HTML tags, and quote wrappers, 35 user stories had no natural language text left. The original Description field looked filled, but the content was 100 percent code, embedded markup, or escape sequences.

These will get the lowest possible clarity and completeness score in the scoring notebook.

### Finding 16. 540 stories are exact duplicates inside the same project

Using the cleaned Title plus Description as the duplicate key, I found 164 groups of identical stories, totaling 540 rows. The average group size is 3.3.

Clearest example: Spring XD has four copies of the same story called "Fix 'cluster/containers' REST endpoint with security enabled", each with 3 Story Points. They were filed within three minutes of each other. Three were closed as Done. One was left in To Do.

Most likely cause: a tool glitch or a copy paste accident.

Implication for the dashboard: duplicate stories inflate sprint velocity. Velocity is a measure of work done per sprint. Scrum Masters need to see them.

### Finding 17. About one third of estimated stories use non Fibonacci values

23.9 percent of all stories carry a Story Point value that is not on the canonical Fibonacci scale. Looking only at stories that have any estimate, the share rises to about one in three. The most common non Fibonacci values are 4, 6, and 10. These are typical of teams that use a linear scale rather than running Planning Poker sessions.

This finding will become a per project metric in the dashboard, so a team can see at a glance whether their estimation practice matches Planning Poker.

## Open questions for later notebooks

- Is there a correlation between Story Point and description length? Do bigger stories also have longer text?
- Do projects differ significantly in their average quality scores once we have computed them?
- Do stories with longer resolution times have lower clarity scores?
- Of the 540 duplicate rows, how many are tool glitches and how many are deliberate?

### Finding 18. Explicit acceptance criteria are essentially absent from this dataset

Only 228 stories (0.7 percent) contain an explicit acceptance criteria signal. The check looks for the literal phrase "acceptance criteria", the abbreviation "AC:", the Behavior Driven Development structure "GIVEN ... WHEN ... THEN", or markdown checklist markers like `- [ ]`.

This is even rarer than the full Cohn template (1.0 percent, Finding 9).

Reference for the importance of acceptance criteria: Mike Cohn's "Conditions of Satisfaction" and Ron Jeffries' "Confirmation" pillar of the three Cs (Card, Conversation, Confirmation).

Interpretation: most teams in this dataset capture user stories as plain prose and rely on the team's shared understanding rather than written tests-of-done. From a QA perspective this is a serious gap. The team has no objective record of when a story is complete, which forces rework and ambiguity in sprint planning.

Implication for the dashboard: a "missing acceptance criteria" tag will be one of the strongest weights in the quality score.