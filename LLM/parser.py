import re


FIELD_PATTERN = re.compile(
    r"^\s*[-*]\s*"
    r"\*{0,2}"
    r"([A-Za-z][A-Za-z0-9 /_\-&]+?)"
    r"\*{0,2}"
    r"\s*[:：]\s*"
    r"\*{0,2}"
    r"\s*"
    r"(.*?)"
    r"\s*$",
    re.MULTILINE,
)

TABLE_ROW_PATTERN = re.compile(
    r"^\s*\|\s*\*{0,2}([A-Za-z][A-Za-z0-9 /_\-&]+?)\*{0,2}\s*\|\s*(.*?)\s*\|\s*$",
    re.MULTILINE,
)


FIELD_ALIASES = {
    "project_purpose":       ["project purpose", "purpose"],
    "project_lead":          ["project lead", "lead"],
    "current_robot_cost":    ["current robot cost", "current cost"],
    "target_cost":           ["target cost"],
    "technology_stack":      ["technology stack", "tech stack"],
    "robotics_meeting_day":  ["robotics group meeting day and time",
                              "robotics meeting day and time",
                              "meeting day and time",
                              "meeting day"],
    "robotics_meeting_time": ["robotics group meeting day and time",
                              "robotics meeting day and time",
                              "meeting day and time",
                              "meeting time"],
    "distribution_plan":     ["distribution/manufacturing plan",
                              "distribution plan",
                              "manufacturing plan",
                              "distribution"],
    "proposed_change":       ["proposed change", "considering moving"],
    "change_effective":      ["change effective"],
}


def clean_value(v: str) -> str:
    v = v.strip()
    v = re.sub(r"\*+", "", v)
    return v.strip()


def parse_model_output(output: str) -> dict:
    fields = {}

    # 1.list
    for m in FIELD_PATTERN.finditer(output):
        name = re.sub(r"\s+", " ", m.group(1).strip().lower())
        value = clean_value(m.group(2))
        if name and value:
            fields[name] = value

    # sheet
    for m in TABLE_ROW_PATTERN.finditer(output):
        name = re.sub(r"\s+", " ", m.group(1).strip().lower())
        if name in ("field", "details", "---", "field name", "value"):
            continue
        if name not in fields:
            value = clean_value(m.group(2))
            if value:
                fields[name] = value

    return fields


def find_field_value(raw_fields: dict, gt_key: str) -> str:
    """从 raw_fields 找 GT key 对应的值"""
    aliases = FIELD_ALIASES.get(gt_key, [gt_key])
    for raw_name, value in raw_fields.items():
        raw_norm = raw_name.replace("_", " ").strip()
        for alias in aliases:
            if alias in raw_norm:
                return value
    return ""


def split_meeting_value(value: str) -> tuple:
    if not value:
        return "", ""
    if ";" in value:
        parts = value.split(";", 1)
        return parts[0].strip(), parts[1].strip()
    return value.strip(), value.strip()    