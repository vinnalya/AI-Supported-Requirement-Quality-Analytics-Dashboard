# References

Sources used to define the user story quality framework in this project.

---

## 1. Mountain Goat Software — User Stories

Industry-standard reference for the classic user story template and the three pillars (Card, Conversation, Confirmation) introduced by Ron Jeffries (2001).

- URL: https://www.mountaingoatsoftware.com/agile/user-stories
- Author: Mike Cohn
- Key contributions used in this project:
  - The classic template: **"As a <type of user>, I want <some goal> so that <some reason>."**
  - The three Cs: Card, Conversation, Confirmation
  - Conditions of Satisfaction = high-level acceptance criteria
  - INVEST mnemonic (Independent, Negotiable, Valuable, Estimatable, Small, Testable)

Used as the **practitioner reference** for defining what a "good" user story looks like.

---

## 2. Lucassen et al. — Quality User Story (QUS) Framework

Peer-reviewed academic framework with 13 quality criteria for user stories, evaluated on 1,023 stories from 18 organizations.

- Title: *Improving agile requirements: the Quality User Story framework and tool*
- Authors: Garm Lucassen, Fabiano Dalpiaz, Jan Martijn E. M. van der Werf, Sjaak Brinkkemper
- Journal: Requirements Engineering, Vol 21, pp. 383–403 (2016)
- DOI: https://doi.org/10.1007/s00766-016-0250-x
- License: Open Access (CC BY 4.0)

### QUS criteria mapped to this project

| QUS criterion | Category | Used in this project for |
|---|---|---|
| Well-formed | Syntax | Detecting missing role / means |
| Atomic | Syntax | Detecting multi-feature stories |
| Minimal | Syntax | Detecting noise in story text |
| Conceptually sound | Semantic | Validating means/ends structure |
| Problem-oriented | Semantic | Catching implementation hints in story text |
| Unambiguous | Semantic | Clarity scoring |
| Full sentence | Syntax | Clarity scoring |
| Estimatable | Pragmatic | Scope risk scoring |
| Unique | Pragmatic (set) | Duplicate detection (future) |
| Uniform | Pragmatic (set) | Format consistency (future) |
| Independent | Pragmatic (set) | Dependency detection (future) |
| Complete | Pragmatic (set) | Coverage gaps (future) |
| Conflict-free | Pragmatic (set) | Conflict detection (future) |

QUS is the **academic foundation** for the quality dimensions used in `04_quality_scoring.ipynb` (later phase).

### Relevance for the AI-supported scoring

The Lucassen paper also introduces AQUSA, an NLP-based tool that detects QUS violations. This is the closest academic precedent to the AI-supported analysis planned in `06_ai_scoring.ipynb`. AQUSA achieves 93.8% recall on syntactic criteria but cannot evaluate semantic criteria reliably without deep language understanding — which motivates the use of modern LLMs in this project.

---

## How these sources are used

1. **For framework design** — the 13 QUS criteria define which quality dimensions get a numeric score.
2. **For rule definitions** — the rule-based scoring (notebook 05) implements the syntactic and a few pragmatic QUS criteria, similar to AQUSA v1.
3. **For the AI-supported analysis** — the LLM prompts (notebook 06) are grounded in the QUS framework and Mountain Goat's classic template, so the model's feedback is consistent with established practice.
4. **For the case study** — findings are interpreted in the language of these two sources so readers can verify against existing literature.