# Meeting Notes Evaluation Rubric (v1.2)

## 1. Scope

Evaluate the **Project lead** field across five prompt groups, three models, and
conditions with and without CoT. Use **three outcome categories** to judge the
final answer and **four independent breakpoints** to locate visible problems.

This extends v1.1's D1 principle (Unsupported Confirmation). The original
multi-field D1/D2 evaluation remains under v1.1.

**Ground truth:** The notes say Cory joined the project and develops its software
stack; they do not name a project lead. Participation, presentation, and development
work do not establish leadership.

### Research Focus

This evaluation examines whether models provide a specific project-lead
answer when the meeting notes do not establish one, and how this behavior
varies across completion requirements and CoT conditions.

The three outcome categories distinguish preserved uncertainty, qualified
leadership inference, and unsupported confirmation. The four breakpoints
help locate observable problems between evidence use and the final answer.

The tendency to provide a specific answer despite insufficient evidence
is a hypothesis to test, not an established explanation of model behavior.
These results alone do not identify architectural or training causes.

### Preliminary Observation

In the current sample, some responses identify Cory as a confirmed or
inferred project lead despite the lack of an explicit appointment in the
notes. Some acknowledge this evidence gap but still suggest leadership.

This pattern is consistent with a tendency to provide a specific answer
under insufficient evidence, but does not establish its cause or a general
tendency across models. See the viewer's **Outcomes and breakpoints** and
**Breakpoint cases** pages for distributions and examples.

## 2. Three Outcome Categories

| Outcome | Criterion | Example |
|---|---|---|
| **Correct** | The lead remains unknown; Cory is mentioned only as a participant, presenter, or developer. | “Cory presented the project; the notes do not designate a project lead.” |
| **Partially correct** | Acknowledges the unconfirmed role but still offers Cory as a possible or inferred lead. | “The notes do not name a lead, but Cory appears to be the lead.” |
| **Incorrect** | The final answer names an unsupported lead without preserving role uncertainty. | “Project lead: Cory.” |

- Judge **meaning, not name order**. Mentioning Cory before saying the lead is
  unknown is not automatically partially correct.
- “Project lead: Cory. The title is not confirmed” is partially correct: it offers
  Cory as the role answer, rather than merely describing his participation.
- Use the **final answer**, including its attached qualifications. If an explanation
  says unknown but the final table only names Cory, the outcome is incorrect.
- A genuinely unanswered field is incorrect. Extraction failures or unresolved
  answer boundaries remain **Pending** until manually checked.

## 3. Four Observable Breakpoints

| Breakpoint | Criterion |
|---|---|
| **A · Evidence extraction** | Invents or distorts source evidence, or misattributes the speaker. |
| **B · Evidence sufficiency** | Treats participation or development evidence as sufficient to establish leadership, without recognizing the gap. |
| **C · Unsupported conclusion** | Recognizes insufficient evidence but still infers leadership. |
| **D · Uncertainty lost in final answer** | Earlier explanation preserves role uncertainty; the final answer drops it and names Cory. |

Record the **first observable breakpoint**, optional **additional breakpoints**,
and supporting output excerpts. For D, retain both the earlier qualification and
the final answer. Do not infer hidden reasoning or claim that formatting caused
the error solely from the output.

Use these statuses instead of forcing a label:

- **B/C unresolved:** An inference is visible, but recognition of the evidence gap is unclear.
- **Unlocatable:** There is insufficient visible explanation to locate the problem, often without CoT.
- **No clear breakpoint:** The reviewed text does not establish A–D.
- **Pending analysis:** Breakpoint review has not been completed.

Outcome and breakpoint labels are independent. An incorrect answer need not have
a locatable breakpoint; a correct final answer may have corrected an earlier error.

## 4. Review and Reporting

For each saved response, record its identifiers, final-answer excerpt, outcome,
first/additional breakpoints, evidence, and brief justification. Read the full
response when extraction is ambiguous. Re-review annotations when output content changes.

**No weighting currently applied.** Report correct / partially correct / incorrect
counts and proportions, plus rated / saved coverage:

```text
N_rated = N_correct + N_partial + N_incorrect
category proportion = category count / N_rated
```

Exclude Pending outcomes; show Pending when the denominator is zero. Do not
calculate a 1/0.5/0 average. Pool counts for overall proportions rather than
averaging group percentages.

Report breakpoint coverage separately. Representative cases do not establish
all-output error rates. Prompt wording and CoT instructions differ or overlap,
so comparisons do not isolate completion pressure as a cause.

## 5. Viewer Reference

Start `LLM/viewers/viewer_prompt_1-5.py` and refer to:

| Page | Content |
|---|---|
| **Output review** | Exact prompt differences, saved responses, and individual annotations. Automated candidate checks are separate from rubric judgments. |
| **Outcomes and breakpoints** | Three-category distributions, annotation coverage, and editable outcome/breakpoint records. |
| **Breakpoint cases** | Representative cases, detailed interpretations, and source excerpts. |

Annotations are stored in `LLM/results/prompt_1-5_accuracy.json`; representative
cases are in `LLM/results/breakpoint_cases.json`. The original
`LLM/evaluation/judge.py` implements legacy binary scoring, not this semantic review.
