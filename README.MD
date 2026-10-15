# LLM Failure Evaluation

Evaluate LLM responses against structured ground truth for missing-information and conflicting-source tasks.

## What's here

- `prompts/` — evaluation prompts
- `outputs/` — model outputs
- `ground_truth/` — ground truth JSON files
- `scoring.csv` — **item-level scoring results**
- `viewer.py` — Streamlit viewer for reviewing results
- `MEETING_NOTES_RUBRIC_v1.md` — current atomic scoring rubric

## Scoring

`scoring.csv` contains item-level evaluation results.

Columns:

- `case_id`, `doc_type`, `task_id`, `model` — case identifiers
- `item` — Info_Item being evaluated
- `gt_status` — ground truth status (Present / Partial / Missing / Distractor)
- `gt_evidence` — supporting evidence from the source document
- `field_value` — model response for the evaluated item
- `score` — atomic score (0 or 1)
- `failure_tag` — failure category assigned during scoring
- `case_final` — aggregate score for the case
- `overall_tags` — failure tags observed in the case

## Rubric

The current rubric uses two atomic dimensions:
- **D1: Unsupported Confirmation** — whether the model gives a definite answer when the source evidence is Missing or Partial.
- **D2: Evasion** — whether the model claims information is missing when it is explicitly supported by the source.
Full definitions and scoring rules are documented in `MEETING_NOTES_RUBRIC_v1.md`.

## How to run

```bash
python build_gt.py
python judge.py
streamlit run viewer.py