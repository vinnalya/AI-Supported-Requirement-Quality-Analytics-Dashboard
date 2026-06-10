# Findings & Insights

This document tracks key insights discovered during data exploration and analysis.
Findings will be referenced in the final case study.

---

## Notebook 01 — Data Understanding (Initial Exploration)

**Date:** Session 1 — Data understanding phase
**Dataset:** TAWOS v1.1 — 458,232 issues from 39 open-source projects
**Working subset:** 31,394 issues filtered to `Type = 'Story'`

### Finding 1 — Dataset is dominated by Bug-type issues
- Bugs make up **47%** of all issues (215,570 out of 458,232).
- Only **6.85%** are typed as "Story" (31,394 issues).
- **Business implication:** Even in mature open-source projects, formal user story authoring is the minority. Quality work on backlog items is critical.

### Finding 2 — A single project dominates the user-story pool
- **Lsstcorp Data Management** contributes **19,578 stories — 62%** of all Story-type issues.
- The remaining 21 projects share 11,816 stories.
- **Risk:** Cross-project insights may be biased by Lsstcorp.
- **Mitigation:** Keep all stories in scope, expose `Project_Name` as a dashboard filter so users can include/exclude Lsstcorp.

### Finding 3 — Missing Description is a real quality issue
- **13%** of user stories (~4,067) have no Description or Description_Text at all.
- These stories ship with just a Title — insufficient context for development.
- **This itself is a quality signal:** "missing description" will become an issue tag in the scoring framework.

### Finding 4 — Story Point is unevenly captured
- **31%** of stories (9,661) have no Story Point estimate.
- Where present, distribution is healthy: median = 3, 75th percentile = 5 (Fibonacci-like).
- **Outlier alert:** one story has Story_Point = 105 — scope risk indicator.
- **13%** of stories had Story_Point changed after initial estimation → unstable estimation = a quality signal.

### Finding 5 — Priority field is largely unusable
- **62%** of stories (19,582) have no Priority assigned.
- **Decision:** Exclude Priority from quality scoring; not enough signal.

### Finding 6 — Data has text artifacts that require cleaning
- Title strings are wrapped in literal double quotes: `"Fix stream failover "`.
- Description_Text fields are prefixed with triple quotes: `"""See https://..."`.
- Trailing whitespace observed in titles.
- **Action:** Regex-based cleaning in notebook `02_data_cleaning.ipynb`.

### Finding 7 — Resolution Time spans an extreme range
- Median resolution time: ~14 days (reasonable sprint window).
- Max resolution time: **~8 years** (4.3M minutes) → forgotten/zombie stories.
- 25th percentile: ~6 hours (small fixes labeled as Story).
- **Investigation needed:** Are very-quick-resolution items real user stories or mislabeled?

### Finding 8 — Data spans 11 years
- Date range: **August 2009 → October 2020**.
- Enables time-series analysis of quality trends over years.

---

## Open Questions (to investigate in next notebooks)

- What % of stories follow the classic **"As a [user], I want [feature], so that [benefit]"** format?
- Is there a correlation between Story_Point and Description length?
- Do projects differ significantly in their average quality scores?
- Do stories with longer resolution times have lower clarity?


### Finding 9 — Less than 1% of user stories follow the canonical Cohn template

Analyzing 31,394 issues officially typed as `Story`:

| Pattern check | Stories | Share |
|---|---:|---:|
| Has any description (non-empty) | 27,327 | 87.0% |
| Has "As a / As an" (role marker) | 2,390 | 7.6% |
| Has "I want / need / would like / ..." (means marker) | ~3,800 | ~12% |
| Has "so that ..." (reason marker) | 1,235 | 3.9% |
| **QUS Well-formed (role + means)** | **871** | **2.8%** |
| **Full Cohn template (role + means + reason)** | **284** | **0.9%** |

Reference for the canonical template: Mountain Goat Software / Mike Cohn — *"As a <type of user>, I want <some goal> so that <some reason>."*
Reference for the "Well-formed" criterion: Lucassen et al. (2016), QUS framework.

**Interpretation:** Even in mature open-source projects where issues are deliberately filed as "User Story", the canonical agile template is almost absent in the description field. Most teams write user stories as plain feature descriptions or bug-like narratives.

**Business impact:** Without the explicit *role / want / reason* structure, downstream readers (developers, QA, BAs) must infer who the user is and why the feature matters. This is exactly the kind of ambiguity that drives sprint rework.

**Caveat:** Some teams may capture the canonical structure in **Title** instead of Description, or in a separate field (e.g., Jira's "User Story" custom field) not present in TAWOS. This analysis only inspects the Description text.

**Next step:** Run the same regex check against `Title` to see whether the structure appears there. This will be done in `02_data_cleaning.ipynb` / feature engineering.

**Caveat check (resolved):** Tested whether the canonical structure might appear in `Title` instead. Only 2.4% of titles contain "as a", 2.1% contain "I want", and 0.2% contain "so that". Combining Title and Description, **only 321 stories (1.0%) contain the full Cohn template anywhere** — adding just 37 stories to the 284 found in Description alone. The conclusion stands: the canonical template is essentially absent from this dataset.

### Finding 10 — Story Point values are not consistently Fibonacci

Planning Poker, the de facto standard for agile effort estimation, uses a modified Fibonacci scale: 1, 2, 3, 5, 8, 13, 21, 34... However, in this dataset:

| Value | Count | Fibonacci? |
|---|---:|---|
| 1 | 4,165 | ✓ |
| 2 | 3,648 | ✓ |
| 3 | 2,285 | ✓ |
| **4** | **2,082** | **✗** |
| 5 | 1,643 | ✓ |
| **6** | **1,059** | **✗** |
| 8 | 1,640 | ✓ |

Non-Fibonacci values (4 and 6) together account for ~14% of all estimated stories. This suggests that a meaningful share of teams either bypass Planning Poker or use a linear estimation scale, which signals lower estimation maturity.

**Action:** A future feature `is_fibonacci_sp` will flag whether a story's estimate sits on the canonical scale (1, 2, 3, 5, 8, 13, 21, 34, 55, 89).

### Finding 11 — 75 stories carry Story_Point ≥ 40 (extreme scope risk)

The maximum Story_Point in the dataset is 105 — a single backlog item estimated at roughly 21 sprints of work. In total, 75 stories carry an estimate of ≥40 SP.

**Interpretation:** These are not user stories in the agile sense; they are epics that were never decomposed. They violate the QUS *Estimatable* and Cohn's INVEST *Small* criteria.

**Action:** Stories with SP ≥ 13 will be flagged as `high_scope_risk` in the cleaning notebook. SP ≥ 40 will be flagged as `extreme_scope_risk`.

**Visual evidence (histogram):** The Story Point distribution shows three patterns:
- Strong Fibonacci peaks at 1, 2, 3, 5 and 8 — Planning Poker is the dominant practice
- Significant secondary peaks at 4 and 6 — about 14% of estimates fall on values not in the canonical scale
- A clear dip at 7 (between 6 and 8) suggests teams that *do* use Fibonacci jump straight from 6 to 8
- A peak at 10 — "round number" preference, hallmark of linear (non-Fibonacci) estimation
- A peak at 0 — non-effort placeholders that should not be classified as user stories

### Finding 12 — Canonical-template adoption peaked in 2014–2015 and then collapsed

Looking at the dataset across 11 years (2009–2020):

| Year | Total stories | Has "As a" % | Full Cohn template % | Has Story_Point % |
|---|---:|---:|---:|---:|
| 2010 | 174 | 4.0% | 0.0% | 66.7% |
| 2013 | 1,893 | 8.6% | 0.3% | 69.9% |
| **2014** | **2,346** | **10.9%** | **5.0%** | 74.4% |
| **2015** | **3,676** | **17.4%** | 1.6% | 79.5% |
| 2016 | 3,734 | 4.9% | 0.2% | 75.8% |
| 2017 | 4,873 | 6.3% | 0.3% | 62.6% |
| 2020 | 3,890 | 5.2% | 0.2% | 72.9% |

**The story arc:**

- **2009–2013:** Almost no canonical-template adoption; "User Story" type is just a Jira label.
- **2014–2015 ("the golden age"):** Sharp rise — Cohn template peaks at 5.0%, "As a" prefix peaks at 17.4%. This is the period of peak agile-methodology marketing.
- **2016 onward:** Collapse. Adoption returns to pre-2014 levels and stays there.

**Counter-intuitive finding:** Canonical-template usage did *not* compound over time. After 2015 it declined and never recovered.

**Possible explanations (to investigate in the dashboard):**
1. A small set of projects with disciplined template use dominated early years; later, more projects joined the dataset and diluted the average.
2. Teams continued to label items as "User Story" in Jira but stopped following the format.
3. The 2014–2015 peak corresponds to the height of agile-method marketing; after that, teams reverted to free-form descriptions.

**Positive trend:** Story Point coverage stabilized at ~70% from 2013 onwards — estimation discipline outlived template discipline.

### Finding 13 — Lsstcorp's volume explains the post-2015 template collapse

Cross-project breakdown of canonical template adoption (only projects with ≥100 stories):

| Project | Stories | Has "As a" % | Full Cohn % | Has SP % |
|---|---:|---:|---:|---:|
| MongoDB Compass | 175 | 51.4% | 34.3% | 19.4% |
| Spring XD | 2,593 | 26.5% | 6.1% | 100.0% |
| Hyperledger Indy Node | 349 | 16.6% | 5.4% | 28.9% |
| Sonatype Nexus | 243 | 9.9% | 3.3% | 45.3% |
| DotNetNuke Platform | 402 | 34.6% | 2.7% | 73.9% |
| Hyperledger Fabric | 2,748 | 11.5% | 0.5% | 10.8% |
| **Lsstcorp Data management** | **19,578** | **4.1%** | **0.0%** | **81.3%** |
| Apache Mesos | 151 | 9.3% | 0.0% | 15.2% |
| (others — all 0% Cohn) | | | | |

Lsstcorp — which contributes 62% of all user stories in the dataset — has **zero** stories matching the full Cohn template. Because it dominates the dataset, it single-handedly pulls the overall Cohn adoption rate from a potential 3–6% down to the observed 0.9%.

**Implication for the dashboard:** users will be able to filter out Lsstcorp to see what the rest of the open-source community looks like — and to verify whether the "post-2015 collapse" was a real practice change or a sampling artifact.

### Finding 14 — Cross-project paradoxes reveal where teams fail

Several projects show partial adherence to the user-story template, exposing the *specific* place teams break down:

- **DotNetNuke Platform** — 34.6% start with "As a..." but only 2.7% complete the template. Teams declare a user role but omit the *reason* (the "so that..." clause). This is precisely the *Business Value* failure mode targeted by the QUS criterion *Conceptually sound*.
- **Hyperledger Fabric** — 11.5% have "As a..." but only 10.8% have a story point. The team writes stories but does not estimate them; backlog readiness is incomplete.
- **The Titanium SDK** and **Aptana Studio** — average Story Point ~7.3 vs the dataset median of 3. These projects routinely violate the INVEST *Small* criterion, signaling unsplit epics labeled as stories.
- **Story Point coverage spans 21x** — from 4.7% (Alloy Framework) to 100% (Spring XD). Estimation discipline is wildly inconsistent across teams.

**Recommendation surface:** the dashboard will use these signals to produce per-project advice — *"DotNetNuke: enforce 'so that' clauses"* vs *"Hyperledger Fabric: require estimates before sprint commit"*. This turns the analytics into actionable feedback rather than just numbers.






