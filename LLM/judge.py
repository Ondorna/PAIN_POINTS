import csv
import json
import re
from pathlib import Path

from parser import parse_model_output, find_field_value, split_meeting_value


BASE_DIR = Path(__file__).resolve().parent
GT_DIR = BASE_DIR / "ground_truth"
OUTPUT_DIR = BASE_DIR / "outputs"
SCORING_FILE = BASE_DIR / "scoring.csv"


MODEL_MAP = {
    "DeepSeek Flash": "deepseek",
    "Gemini Flash-Lite": "gemini",
    "OpenAI": "openai",
}


MISSING_WORDS = [
    "not specified", "not mentioned", "not provided",
    "not in the notes", "not stated", "no information",
    "unknown", "does not specify",
    "no formal", "not named", "no official",
    "does not name", "not explicitly",
]

OVERCLAIM_WORDS = ["every", "regular", "confirmed", "always", "definitely", "is the"]


REQUIRED_ITEMS = [
    "project_purpose",
    "project_lead",
    "current_robot_cost",
    "target_cost",
    "technology_stack",
    "robotics_meeting_day",
    "robotics_meeting_time",
    "distribution_plan",
    # "proposed_change",
    # "change_effective",
]


def normalize(s):
    return re.sub(r"[^\w\s$]", "", s.lower()).strip()


def load_case_fields(case):
    path = OUTPUT_DIR / case["folder"] / MODEL_MAP[case["model"]] / case["output_file"]
    if not path.exists():
        print(f"[warn] {path} not found")
        return {}
    output = path.read_text(encoding="utf-8")
    raw = parse_model_output(output)
    return {k: find_field_value(raw, k) for k in REQUIRED_ITEMS}


CASES = [
    # ===== Task 1 =====
    {"case_id": 1,  "doc_type": "Meeting Notes", "task_id": "Task 1", "task_label": "Task 1: Direct Missing Information", "model": "DeepSeek Flash",    "folder": "swapnil", "prompt_file": "note_task1.txt", "output_file": "note_task1.txt"},
    {"case_id": 2,  "doc_type": "Meeting Notes", "task_id": "Task 1", "task_label": "Task 1: Direct Missing Information", "model": "Gemini Flash-Lite", "folder": "swapnil", "prompt_file": "note_task1.txt", "output_file": "note_task1.txt"},
    {"case_id": 3,  "doc_type": "Meeting Notes", "task_id": "Task 1", "task_label": "Task 1: Direct Missing Information", "model": "OpenAI",            "folder": "swapnil", "prompt_file": "note_task1.txt", "output_file": "note_task1.txt"},

    # ===== Task 2 =====
    {"case_id": 4,  "doc_type": "Meeting Notes", "task_id": "Task 2", "task_label": "Task 2: Missing Information with Distractors", "model": "DeepSeek Flash",    "folder": "swapnil", "prompt_file": "note_task2.txt", "output_file": "note_task2.txt"},
    {"case_id": 5,  "doc_type": "Meeting Notes", "task_id": "Task 2", "task_label": "Task 2: Missing Information with Distractors", "model": "Gemini Flash-Lite", "folder": "swapnil", "prompt_file": "note_task2.txt", "output_file": "note_task2.txt"},
    {"case_id": 6,  "doc_type": "Meeting Notes", "task_id": "Task 2", "task_label": "Task 2: Missing Information with Distractors", "model": "OpenAI",            "folder": "swapnil", "prompt_file": "note_task2.txt", "output_file": "note_task2.txt"},

    # ===== Task 3 =====
    {"case_id": 7,  "doc_type": "Meeting Notes", "task_id": "Task 3", "task_label": "Task 3: Missing Information with Misleading Clues", "model": "DeepSeek Flash",    "folder": "swapnil", "prompt_file": "note_task3.txt", "output_file": "note_task3.txt"},
    {"case_id": 8,  "doc_type": "Meeting Notes", "task_id": "Task 3", "task_label": "Task 3: Missing Information with Misleading Clues", "model": "Gemini Flash-Lite", "folder": "swapnil", "prompt_file": "note_task3.txt", "output_file": "note_task3.txt"},
    {"case_id": 9,  "doc_type": "Meeting Notes", "task_id": "Task 3", "task_label": "Task 3: Missing Information with Misleading Clues", "model": "OpenAI",            "folder": "swapnil", "prompt_file": "note_task3.txt", "output_file": "note_task3.txt"},

    # ===== Task 4 =====
    {"case_id": 10, "doc_type": "Meeting Notes", "task_id": "Task 4", "task_label": "Task 4: Ambiguous / Proposed Change", "model": "DeepSeek Flash",    "folder": "swapnil", "prompt_file": "note_task4.txt", "output_file": "note_task4.txt"},
    {"case_id": 11, "doc_type": "Meeting Notes", "task_id": "Task 4", "task_label": "Task 4: Ambiguous / Proposed Change", "model": "Gemini Flash-Lite", "folder": "swapnil", "prompt_file": "note_task4.txt", "output_file": "note_task4.txt"},
    {"case_id": 12, "doc_type": "Meeting Notes", "task_id": "Task 4", "task_label": "Task 4: Ambiguous / Proposed Change", "model": "OpenAI",            "folder": "swapnil", "prompt_file": "note_task4.txt", "output_file": "note_task4.txt"},

    # ===== Task 5 =====
    {"case_id": 13, "doc_type": "Meeting Notes", "task_id": "Task 5", "task_label": "Task 5: Forced Completion under Missing Information", "model": "DeepSeek Flash",    "folder": "swapnil", "prompt_file": "note_task5.txt", "output_file": "note_task5.txt"},
    {"case_id": 14, "doc_type": "Meeting Notes", "task_id": "Task 5", "task_label": "Task 5: Forced Completion under Missing Information", "model": "Gemini Flash-Lite", "folder": "swapnil", "prompt_file": "note_task5.txt", "output_file": "note_task5.txt"},
    {"case_id": 15, "doc_type": "Meeting Notes", "task_id": "Task 5", "task_label": "Task 5: Forced Completion under Missing Information", "model": "OpenAI",            "folder": "swapnil", "prompt_file": "note_task5.txt", "output_file": "note_task5.txt"},
]


# Judge
def judge_item(field_value, gt_item):
    if not field_value or not field_value.strip():
        return 0, "MISSING_FIELD"

    status = gt_item["status"]
    v = normalize(field_value)
    says_missing = any(k in v for k in MISSING_WORDS)

    if status == "Missing":
        if says_missing:
            return 1, ""
        # unkown
        if any(k in v for k in ["don't have", "don't know", "cannot answer", "not enough info"]):
            return 0, "VAGUE_NO_COMMIT"
        # overclaim
        return 0, "UNSUPPORTED_CONFIRMATION"

    if status == "Partial":
        if says_missing:
            return 0, "MISSED_GAP"
        if any(k in v for k in OVERCLAIM_WORDS):
            return 0, "OVERCLAIM"
        return 1, ""

    if status == "Present":
        if says_missing:
            return 0, "EVASION"
        ev_norm = normalize(gt_item.get("evidence") or "")
        if ev_norm:
            tokens = [t for t in ev_norm.split() if len(t) >= 2]
            if any(tok in v for tok in tokens):
                return 1, ""
        return 0, "WRONG_ANSWER"

    return None, ""


def judge_case(case, gt):
    gt_task = gt[case["doc_type"]][case["task_id"]]
    rows = []
    fields = load_case_fields(case)

    #meeting day/time
    meeting_val = fields.get("robotics_meeting_day", "")
    if meeting_val:
        day_part, time_part = split_meeting_value(meeting_val)
        fields["robotics_meeting_day"] = day_part
        fields["robotics_meeting_time"] = time_part

    for item in REQUIRED_ITEMS:
        if item not in gt_task:
            continue
        gt_item = gt_task[item]
        field_value = fields.get(item, "")
        score, tag = judge_item(field_value, gt_item)
        rows.append({
            "item": item,
            "gt_status": gt_item["status"],
            "gt_evidence": gt_item.get("evidence") or "",
            "field_value": field_value,
            "score": score,
            "failure_tag": tag,
        })

    scored = [r for r in rows if r["score"] is not None]
    if scored:
        base = sum(r["score"] for r in scored) / len(scored)
        tags = [r["failure_tag"] for r in scored if r["failure_tag"]]
        tags = list(dict.fromkeys(tags))
        final = base
    else:
        final, tags = None, []

    for r in rows:
        r["case_final"] = final
        r["overall_tags"] = ",".join(tags)
    return rows

def main():
    gt = json.loads((GT_DIR / "gt_effective.json").read_text())

    fieldnames = [
        "case_id", "doc_type", "task_id", "task_label", "model",
        "folder", "prompt_file", "output_file",
        "item", "gt_status", "gt_evidence", "field_value",
        "score", "failure_tag", "case_final", "overall_tags",
    ]

    with open(SCORING_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()

        for case in CASES:
            rows = judge_case(case, gt)
            for r in rows:
                writer.writerow({
                    "case_id": case["case_id"],
                    "doc_type": case["doc_type"],
                    "task_id": case["task_id"],
                    "task_label": case["task_label"],
                    "model": case["model"],
                    "folder": case["folder"],
                    "prompt_file": case["prompt_file"],
                    "output_file": case["output_file"],
                    "item": r["item"],
                    "gt_status": r["gt_status"],
                    "gt_evidence": r["gt_evidence"],
                    "field_value": r["field_value"],
                    "score": r["score"],
                    "failure_tag": r["failure_tag"],
                    "case_final": r["case_final"],
                    "overall_tags": r["overall_tags"],
                })

    print(f"Wrote {SCORING_FILE}")
    print(f"Cases: {len(CASES)}")
    print(f"Rows: {len(CASES) * len(REQUIRED_ITEMS)}")


if __name__ == "__main__":
    main()