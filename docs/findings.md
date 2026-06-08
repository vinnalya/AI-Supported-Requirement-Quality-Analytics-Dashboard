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