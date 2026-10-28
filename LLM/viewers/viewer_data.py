"""Shared outcome and breakpoint data for the English viewer."""
from pathlib import Path
import hashlib
import json

import pandas as pd

SCORE_FILE = Path(__file__).resolve().parent.parent / 'results/prompt_1-5_accuracy.json'
LABELS = ['Pending', 'Correct', 'Partially correct', 'Incorrect']
BREAKPOINTS = ['Pending analysis', 'A', 'B', 'C', 'D', 'B/C unresolved', 'Unlocatable', 'No clear breakpoint']
RUBRIC = 'cory_outcome_breakpoints_v3'


def load_rows(records, output_root, models, variants):
    saved = json.loads(SCORE_FILE.read_text(encoding='utf-8')) if SCORE_FILE.exists() else {}
    rows = []
    for record in records:
        key = record['path'].relative_to(output_root).as_posix()
        digest = hashlib.sha256(record['text'].encode()).hexdigest()
        previous = saved.get(key, {})
        valid = previous.get('sha256') == digest and previous.get('rubric') == RUBRIC
        row = previous if valid else {}
        rows.append({'File': key, 'Model': models[record['model']], 'Prompt': f"P{record['group']}",
                     'Condition': variants[record['variant']], 'Sample': record['sample'],
                     'Outcome': row.get('status', 'Pending'), 'First breakpoint': row.get('first_breakpoint', 'Pending analysis'),
                     'Other breakpoints': ', '.join(row.get('other_breakpoints', [])),
                     'Project lead excerpt': row.get('evidence', ''), 'Breakpoint evidence': row.get('breakpoint_evidence', ''),
                     'Notes': row.get('note', ''), 'sha256': digest})
    return pd.DataFrame(rows)


def summarize(frame):
    counts = {label: int((frame['Outcome'] == label).sum()) for label in LABELS[1:]}
    rated = sum(counts.values())
    return {label: f'{count} ({count / rated:.1%})' if rated else 'Pending' for label, count in counts.items()} | {'Rated / saved': f'{rated} / {len(frame)}'}



CASE_FILE = Path(__file__).resolve().parent.parent / 'results/breakpoint_cases.json'

def load_cases(root):
    cases = json.loads(CASE_FILE.read_text(encoding='utf-8'))
    for case in cases:
        path = root / case['file']
        text = path.read_text(encoding='utf-8') if path.exists() else ''
        case['current'] = path.exists() and hashlib.sha256(text.encode()).hexdigest() == case['sha256']
    return cases

