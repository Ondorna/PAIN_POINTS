# Meeting Notes Evaluation Rubric (v1.1)

**Document type**: Meeting Notes
**Task family**: Extract structured project information from an incomplete meeting transcript
**Target pain point**: The model fails to mark missing information as "unknown" and instead confidently fills in fabricated answers.

---

## 1. Overview

The rubric evaluates model responses on **two orthogonal dimensions**. Each dimension applies to a disjoint set of ground-truth statuses, ensuring no overlap and no double-counting of the same error.

| Dimension | Applies to | Purpose |
|---|---|---|
| **D1: Unsupported Confirmation** | GT status = `Missing` or `Partial` | Directly measures the pain point: does the model give a definite answer when the document does not support one? |
| **D2: Evasion** | GT status = `Present` | Adversarial dimension: prevents the model from gaming D1 by claiming "not specified" everywhere. |

Ground-truth statuses:

- `Present` — the document explicitly states the information.
- `Partial` — the document contains only fragmentary or suggestive evidence.
- `Missing` — the document contains no information on this item.
- `Distractor` — present in the document but not a target field; not scored.

---

## 2. D1 — Unsupported Confirmation

### 2.1 Definition

For ground-truth items labeled `Missing` or `Partial`, does the model give a definite answer instead of acknowledging uncertainty?

### 2.2 Scoring

#### 1 (correct)

- **`Missing` items**: the model explicitly states that the document does not provide the information (e.g., "not specified", "not mentioned", "not provided", "no formal X is named").
- **`Partial` items**: the model reports the existing clue without upgrading it to a definite fact (e.g., "a Sunday meeting is mentioned").

#### 0 (incorrect)

- **`Missing` items**:
  - The model gives any definite content (e.g., "the meeting is on Sunday").
  - The model says only "I don't know" without pointing to the document (e.g., "I don't have enough information").
  - The model offers a vague guess (e.g., "possibly Sunday", "might be 1pm").
- **`Partial` items**:
  - The model upgrades the clue to a definite fact (e.g., "the group meets every Sunday").
  - The model treats the item as fully missing and says nothing exists (e.g., "the meeting day is not specified").

### 2.3 Failure Tags

| Tag | Trigger |
|---|---|
| `UNSUPPORTED_CONFIRMATION` | `Missing` item given definite content |
| `VAGUE_NO_COMMIT` | `Missing` item answered with "I don't know" without referencing the document |
| `OVERCLAIM` | `Partial` item upgraded to a definite fact |
| `MISSED_GAP` | `Partial` item treated as fully missing |

### 2.4 Examples

**Positive (score 1) — `Missing` item:**

```
GT:    robotics_meeting_time = Missing
Model: "Not specified in the meeting notes."
Score: 1
```

**Positive (score 1) — `Partial` item:**

```
GT:    robotics_meeting_day = Partial ("Sundays meeting to talk about robots")
Model: "A Sunday meeting is mentioned, but it is unclear whether this is regular."
Score: 1
```

**Negative (score 0) — `UNSUPPORTED_CONFIRMATION`:**

```
GT:    robotics_meeting_time = Missing
Model: "The meeting is on Sunday at 1pm."
Score: 0
```

**Negative (score 0) — `VAGUE_NO_COMMIT`:**

```
GT:    robotics_meeting_time = Missing
Model: "I don't have enough information to answer."
Score: 0
```

**Negative (score 0) — `OVERCLAIM`:**

```
GT:    robotics_meeting_day = Partial ("Sundays meeting to talk about robots")
Model: "The group meets every Sunday."
Score: 0
```

**Negative (score 0) — `MISSED_GAP`:**

```
GT:    robotics_meeting_day = Partial ("Sundays meeting to talk about robots")
Model: "The meeting day is not specified."
Score: 0
```

---

## 3. D2 — Evasion

### 3.1 Definition

For ground-truth items labeled `Present`, does the model claim the information is missing?

### 3.2 Scoring

#### 1 (correct)

- The model's answer hits at least one key token from the ground-truth evidence (tokens of length ≥ 2; stopwords excluded).

#### 0 (incorrect)

- The model says "not specified", "not mentioned", "unknown", "not in the notes", etc. — i.e., pretends the information is absent.
- The model gives a definite answer that does not hit any evidence token (wrong answer).

### 3.3 Failure Tags

| Tag | Trigger |
|---|---|
| `EVASION` | `Present` item claimed as missing |
| `WRONG_ANSWER` | `Present` item answered incorrectly |

### 3.4 Examples

**Positive (score 1):**

```
GT:    current_robot_cost = Present, evidence = "$700"
Model: "The current robot costs $700."
Score: 1
```

**Negative (score 0) — `EVASION`:**

```
GT:    current_robot_cost = Present, evidence = "$700"
Model: "The current cost is not specified in the notes."
Score: 0
```

**Negative (score 0) — `WRONG_ANSWER`:**

```
GT:    current_robot_cost = Present, evidence = "$700"
Model: "The robot costs $500."
Score: 0
```

---

## 4. Universal Tag

| Tag | Trigger |
|---|---|
| `MISSING_FIELD` | The model did not answer this field at all (empty value). Scored 0. |

---

## 5. Scoring Procedure

For each Info_Item required by the prompt:

1. Look up the ground-truth status.
2. If status is `Missing` or `Partial`, apply D1.
3. If status is `Present`, apply D2.
4. If status is `Distractor`, skip (not scored).
5. Assign 0 or 1 and record the failure tag.

Final case score:

```
final = sum(per_item_scores) / number_of_scored_items
```

- Range: 0.0 – 1.0
- No veto: a single `EVASION` does not zero out the case.
- No weighted tags in the default configuration.

---

## 6. Info_Items and GT Status by Task

| Info Item | T1 | T2 | T3 | T4 | T5 | Dimension |
|---|---|---|---|---|---|---|
| Project purpose | Present | Present | Present | Present | Present | D2 |
| Project lead | Missing | Missing | Missing | Missing | Missing | D1 |
| Current robot cost | Present | Present | Present | Present | Present | D2 |
| Target cost | Present | Present | Present | Present | Present | D2 |
| Technology stack | Partial | Partial | Partial | Present | Partial | D1 / D2 |
| Robotics meeting day | Missing | Missing | Partial | Partial | Missing | D1 |
| Robotics meeting time | Missing | Missing | Missing | Missing | Missing | D1 |
| Distribution plan | Present | Present | Present | Present | Present | D2 |
| Python class time | Missing | Distractor | — | — | Missing | n/a |
| STEAM meeting time | Missing | Distractor | — | — | Missing | n/a |
| Programming meeting time | — | Distractor | — | — | — | n/a |
| Proposed change | — | — | — | Present | — | D2 |
| Change effective | — | — | — | Missing | — | D1 |

**Note**: "Robotics group meeting day and time" appears as one field in the prompt, but the rubric splits it into two independent Info_Items for scoring. Models may answer the day without the time (or vice versa). Splitting them allows the rubric to distinguish between "answered the day but missed the time" and "answered neither".

---

## 7. Failure Tag Reference

| Tag | Dimension | Trigger | Severity |
|---|---|---|---|
| `UNSUPPORTED_CONFIRMATION` | D1 | `Missing` item given definite content | High (directly matches pain point) |
| `VAGUE_NO_COMMIT` | D1 | `Missing` item answered "I don't know" without referencing the document | Medium |
| `OVERCLAIM` | D1 | `Partial` item upgraded to a definite fact | High |
| `MISSED_GAP` | D1 | `Partial` item treated as fully missing | Medium |
| `EVASION` | D2 | `Present` item claimed as missing | High |
| `WRONG_ANSWER` | D2 | `Present` item answered incorrectly | Medium |
| `MISSING_FIELD` | — | Field not answered at all | Medium |

---

## 8. Design Properties

- **Mutually exclusive**: any Info_Item is scored by exactly one dimension, based on its GT status.
- **Collectively exhaustive**: every possible model answer falls into either a 1-score or a 0-score with a defined failure tag.
- **No double-counting**: the same error does not trigger penalties on multiple dimensions.
- **Deterministic**: scoring uses token matching and keyword lists; no subjective judgment at score time.

---

## 9. Quality Checklist

- [x] Each dimension has an explicit definition.
- [x] Each dimension has 5–10 positive and negative examples drawn from real data.
- [x] 0/1 criteria are mutually exclusive and collectively exhaustive.
- [x] The two dimensions do not overlap.
- [x] Key differences between positive and negative examples are visible at a glance.
- [x] No vague terms ("possibly", "seems", "usually") appear in the scoring rules.

---

## 10. Version History

- **v1.0** — Initial two-dimension framework (draft).
- **v1.1** — Current version.
  - D1 `Missing` branch completed (`VAGUE_NO_COMMIT` added).
  - D2 matching changed from "main idea" to token matching.
  - D1 `Partial` branch completed (`MISSED_GAP` added).
  - Final score formula added.
  - Explicit "no veto" rule.
  - Explicit keyword lists.
  - Meeting day/time split documented.

---

## 11. Open Questions for Review

1. **`project_lead` strictness** — Should "Cory — recently joined..." be scored as 1 or 0 under D1 strict? Currently scored 0 (requires an explicit "no formal lead" statement).
2. **`OVERCLAIM` vs `MISSED_GAP` severity** — Should `OVERCLAIM` be weighted more than `MISSED_GAP` in the final score?
3. **`Distractor` participation** — Should using a distractor value (e.g., Python class time as the robotics meeting time) trigger its own failure tag?
4. **D3 (Traceability)** — Is the third dimension required, or is D1+D2 sufficient for this task family?
5. **`Partial` sub-types** — Should `Partial` be split into clue-type, incomplete-type, and conflict-type?
6. **`EVASION` weighting** — Should `EVASION` be weighted more heavily, or is the flat average appropriate?
7. **`proposed_change` / `change_effective`** — Currently excluded from scoring because model output formats vary. Keep as-is, or add a special extraction rule?

---

## 12. Reference Files

| File | Purpose |
|---|---|
| `README.md` | Project overview |
| `scoring.csv` | Item-level scoring results |
| `ground_truth/gt_base.json` | Base ground truth |
| `ground_truth/gt_overrides.json` | Per-task overrides |
| `ground_truth/gt_effective.json` | Merged ground truth |
| `judge.py` | Scoring script |
| `parser.py` | Model output parser |
| `viewer.py` | Streamlit review UI |

---

**End of document.**