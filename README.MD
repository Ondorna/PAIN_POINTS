# LLM Failure Evaluation

Evaluate LLM responses against structured ground truth for missing-information and conflicting-source tasks.

## What's here

- `prompts/` — evaluation prompts
- `outputs/` — model outputs
- `ground_truth/` — ground truth JSON files
- `LLM/results/` — item-level scores, outcome ratings, and case reviews
- `LLM/viewers/viewer_prompt.py` — original viewer for item-level scoring, prompts, and model responses
- `LLM/viewers/viewer_prompt_1-5.py` — five-prompt comparison, outcome distributions, and breakpoint cases
- `LLM/rubics/MEETING_NOTES_RUBRIC_v1.1.md` — current atomic scoring rubric

## File organization

- `LLM/viewers/` — Streamlit interfaces and data loading
- `LLM/evaluation/` — parsing, scoring, ground-truth building, and inspection tools
- `LLM/runners/` — model API scripts; read credentials from `LLM/.env`
- `LLM/results/` — scoring CSVs and review JSON files
- `LLM/rubics/` — scoring rubrics

Existing `prompts/`, `outputs/`, `ground_truth/`, and local `EN/` folders remain in place.

## Scoring

The original evaluation uses `LLM/rubics/MEETING_NOTES_RUBRIC_v1.1.md`;
the five-prompt 4 + 3 framework is defined in `LLM/rubics/MEETING_NOTES_RUBRIC_v1.2.md`.

### Original evaluation — item-level scoring

`LLM/results/scoring.csv` stores scores for individual fields against ground truth,
including source evidence, model answers, failure tags, and aggregate case scores.
Atomic scores are 0 or 1. View these results in `viewer_prompt.py`.

The original rubric checks unsupported confirmation when evidence is missing or
partial, and evasion when information is present. See
`LLM/rubics/MEETING_NOTES_RUBRIC_v1.1.md` for the scoring rules.

### Five-prompt experiment — Project lead scoring

`LLM/results/prompt_1-5_accuracy.json` stores ratings for the **Project lead field only**,
across three models, five prompts, and conditions with and without CoT.
View these results in `viewer_prompt_1-5.py`.

- **Correct:** The lead is unknown; Cory is mentioned only as a participant,
  presenter, or developer.
- **Partially correct:** Acknowledges the unconfirmed role but still offers Cory
  as a possible or inferred lead.
- **Incorrect:** The final answer names Cory without preserving uncertainty.
  An unanswered lead field is also incorrect; parsing failures remain pending.

Ratings follow meaning rather than the order in which Cory is mentioned.
No weighting or 1/0.5/0 average is currently applied. The overview shows counts
and proportions for all three outcomes, excluding pending ratings. Changes to an
output invalidate its saved rating.

Each output also has an independent first-breakpoint annotation, optional
additional breakpoints, and evidence. Fifteen representative CoT cases are
annotated; other CoT outputs await analysis, and non-CoT outputs are currently
marked unlocatable. Breakpoint labels do not determine outcome ratings.

`LLM/results/breakpoint_cases.json` contains 15 representative CoT cases labeled by visible
breakpoints: evidence extraction (A), evidence sufficiency (B), unsupported
conclusion (C), and uncertainty lost in the final answer (D). These case labels
are separate from outcome ratings and do not measure all-output failure rates.

## How to run

From the repository root:

```bash
python -m pip install streamlit pandas
```

Original viewer — review `scoring.csv`, ground truth, prompts, and model responses:

```bash
streamlit run LLM/viewers/viewer_prompt.py
```

Five-prompt viewer — compare completion pressure and CoT, review Project lead
outcomes (correct / partially correct / incorrect), and inspect representative breakpoint cases:

```bash
streamlit run LLM/viewers/viewer_prompt_1-5.py
```

To regenerate the original scoring results:

```bash
python LLM/evaluation/build_gt.py
python LLM/evaluation/judge.py
```
