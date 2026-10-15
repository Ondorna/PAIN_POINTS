import csv
import sys

TARGET = sys.argv[1:] if len(sys.argv) > 1 else [str(i) for i in range(1, 16)]

with open('scoring.csv') as f:
    rows = list(csv.DictReader(f, delimiter='\t'))

for cid in TARGET:
    print(f"===== case {cid} =====")
    for r in rows:
        if r['case_id'] == cid:
            item = r['item']
            gt = r['gt_status']
            val = r['field_value']
            score = r['score']
            tag = r['failure_tag']
            print(f"  {item:24} GT={gt:8} score={score} tag={tag:20} val={val!r}")
    print()