# Analysis Decisions Log

This document tracks the analysis decisions made during the project, the alternatives considered, and the rationale. Useful for the case study and for reviewers.

---

## D1 — Dataset choice: TAWOS over raw Zenodo dump
**Considered:**
- Zenodo Public Jira Dataset (raw 6.3 TB MongoDB dump, restricted access)
- TAWOS v1.1 (4 GB MySQL dump, public, Apache 2.0 license)

**Decision:** TAWOS.
**Rationale:** TAWOS is the cleaned, structured derivative of the same Jira repositories. It is downloadable, ships with documentation, and is sized appropriately for a portfolio project (458K issues, ~4 GB). The raw Zenodo dump would require MongoDB setup, access requests, and storage we don't need.

---

## D2 — Storage: MySQL over SQLite or flat files
**Decision:** MySQL 8.0 (matches TAWOS dump format).
**Rationale:** TAWOS ships as a MySQL `.sql` dump. Importing into MySQL avoids data conversion losses. Also aligns with project plan Step 7 (SQL Database) and enables Power BI connectivity later.

---

## D3 — Filter strategy: `Type = 'Story'` only
**Considered:**
- (A) Strict: only `Story`
- (B) Broad: Story + New Feature + Enhancement Request
- (C) Including Improvement

**Decision:** Strict — only `Type = 'Story'` (31,394 records).
**Rationale:** Project scope is *user-story* quality, not generic requirement quality. Mixing types would dilute analysis. Can revisit and broaden later if needed.

---

## D4 — Keep Lsstcorp despite dominance
Lsstcorp Data Management contributes 62% of stories.

**Considered:**
- (A) Keep all, expose as filter in dashboard
- (B) Cap Lsstcorp at 5,000 to balance
- (C) Exclude Lsstcorp entirely

**Decision:** (A) Keep all, make `Project_Name` a dashboard filter.
**Rationale:** Discarding data is destructive. Capping introduces sampling bias. Making it filterable lets users see "with Lsstcorp" and "without Lsstcorp" views and judge the impact themselves.

---

## D5 — Keep stories with missing Description
Some 4,067 stories have no Description at all.

**Decision:** Keep them in the dataset, do not drop.
**Rationale:** Missing Description is itself a quality signal. Dropping these rows would erase exactly the kind of low-quality item we're trying to detect. They will receive low quality scores and contribute to "missing_description" issue counts.

---

## D6 — Drop Priority from scoring
Priority is null in 62% of stories.

**Decision:** Exclude Priority from quality framework.
**Rationale:** Insufficient signal density. Including it would introduce noise rather than information.