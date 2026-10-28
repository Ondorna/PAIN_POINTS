import json
from pathlib import Path

GT_DIR = Path(__file__).resolve().parent.parent / "ground_truth"

def build_effective_gt():
    base = json.loads((GT_DIR / "gt_base.json").read_text())
    overrides = json.loads((GT_DIR / "gt_overrides.json").read_text())

    effective = {}
    for doc_type, tasks in overrides.items():
        if doc_type.startswith("_"):
            continue
        effective[doc_type] = {}
        for task_id, override in tasks.items():
            merged = dict(base)
            for item, val in override.items():
                merged[item] = val
            effective[doc_type][task_id] = merged

    (GT_DIR / "gt_effective.json").write_text(
        json.dumps(effective, indent=2, ensure_ascii=False)
    )
    print(f"Built GT for {sum(len(t) for t in effective.values())} tasks")

if __name__ == "__main__":
    build_effective_gt()