from pathlib import Path
from parser import parse_model_output, find_field_value

REQUIRED = [
    'project_purpose', 'project_lead', 'current_robot_cost', 'target_cost',
    'technology_stack', 'robotics_meeting_day', 'robotics_meeting_time',
    'distribution_plan',
]

path = Path(__file__).resolve().parent.parent / "outputs/swapnil/deepseek/note_task5.txt"
output = path.read_text()
raw = parse_model_output(output)

print(f"=== {path} ===")
print("=== Raw fields parsed ===")
for k, v in raw.items():
    print(f"  {k!r}: {v[:60]!r}")

print()
print("=== Mapped to GT keys ===")
for key in REQUIRED:
    val = find_field_value(raw, key)
    print(f"  {key}: {val[:60]!r}")