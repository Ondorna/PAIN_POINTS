from pathlib import Path
import json
import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent.parent

PROMPT_DIR = BASE_DIR / "prompts"
OUTPUT_DIR = BASE_DIR / "outputs"
SCORING_FILE = BASE_DIR / "results/scoring.csv"
GT_DIR = BASE_DIR / "ground_truth"

MODEL_MAP = {
    "DeepSeek Flash": "deepseek",
    "Gemini Flash-Lite": "gemini",
    "OpenAI": "openai",
}

STATUS_LABEL = {
    "Present": "[P]",
    "Partial": "[~]",
    "Missing": "[M]",
    "Distractor": "[D]",
}

TAG_LABEL = {
    # v1.1
    "UNSUPPORTED_CONFIRMATION": "UNSUPPORTED_CONFIRMATION",
    "VAGUE_NO_COMMIT": "VAGUE_NO_COMMIT",
    "OVERCLAIM": "OVERCLAIM",
    "MISSED_GAP": "MISSED_GAP",
    "EVASION": "EVASION",
    "WRONG_ANSWER": "WRONG_ANSWER",
    "MISSING_FIELD": "MISSING_FIELD",
    "FALSE_ANSWER": "FALSE_ANSWER",
    "UNSUPPORTED_CLAIM": "UNSUPPORTED_CLAIM",
    "CONFLICT_SUPPRESSION": "CONFLICT_SUPPRESSION",
}


#Page Setup
st.set_page_config(
    page_title="LLM Evaluation Viewer",
    page_icon="",
    layout="wide",
)

st.title("LLM Evaluation Viewer")
st.caption(
    "Review source documents, prompts, model responses, "
    "and item-level scoring against ground truth."
)


# ============ Helpers ============
def read_text_file(path: Path) -> str:
    if not path.exists():
        return f"[File not found: {path}]"
    return path.read_text(encoding="utf-8")


@st.cache_data
def load_scoring_file(path_str: str):
    path = Path(path_str)
    if not path.exists():
        st.error(f"Scoring file not found: {path}")
        return None
    try:
        df = pd.read_csv(path, sep="\t", encoding="utf-8")
        if df.shape[1] == 1:
            df = pd.read_csv(path, sep=",", encoding="utf-8")
        df = df.dropna(how="all")
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Could not load scoring.csv: {e}")
        return None


def normalize_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip().lower()


def score_label(score):
    if pd.isna(score):
        return "-"
    try:
        return {1: "1", 0: "0"}.get(int(score), "-")
    except (ValueError, TypeError):
        return "-"


def result_icon(result):
    return {
        "PASS": "PASS",
        "PARTIAL": "PARTIAL",
        "FAIL": "FAIL",
    }.get(str(result).upper(), "-")


#Load scoring
scoring_df = load_scoring_file(str(SCORING_FILE))

if scoring_df is None or scoring_df.empty:
    st.stop()

IS_NEW_FORMAT = {"item", "gt_status", "score"}.issubset(scoring_df.columns)


#Sidebar
st.sidebar.header("Evaluation Selection")

if IS_NEW_FORMAT:
    doc_type = st.sidebar.selectbox(
        "Doc Type",
        sorted(scoring_df["doc_type"].dropna().unique())
    )
    df_doc = scoring_df[scoring_df["doc_type"] == doc_type]

    task_id = st.sidebar.selectbox(
        "Task",
        sorted(df_doc["task_id"].dropna().unique())
    )
    df_task = df_doc[df_doc["task_id"] == task_id]

    model_name = st.sidebar.selectbox(
        "Model",
        sorted(df_task["model"].dropna().unique())
    )
    df_model = df_task[df_task["model"] == model_name]

    case_ids = sorted(
        df_model["case_id"].dropna().unique(),
        key=lambda x: int(x) if str(x).isdigit() else 0
    )
    case_id = st.sidebar.selectbox("Case", case_ids)
    selected_rows = df_model[df_model["case_id"] == case_id]

    if selected_rows.empty:
        st.warning("No rows found for selection.")
        st.stop()
    selected_row = selected_rows.iloc[0]

    folder = selected_row.get("folder", selected_row.get("Folder", ""))
    prompt_file = selected_row.get("prompt_file", selected_row.get("Prompt File", ""))
    output_file = selected_row.get("output_file", selected_row.get("Output File", ""))

else:
    failure_type = st.sidebar.selectbox(
        "Failure Type",
        scoring_df["Failure Type"].dropna().unique()
    )
    df_f = scoring_df[scoring_df["Failure Type"] == failure_type]

    case_name = st.sidebar.selectbox(
        "Case",
        df_f["Case"].dropna().unique()
    )
    df_c = df_f[df_f["Case"] == case_name]

    task_name = st.sidebar.selectbox(
        "Task",
        df_c["Task"].dropna().unique()
    )
    df_t = df_c[df_c["Task"] == task_name]

    model_name = st.sidebar.selectbox(
        "Model",
        df_t["Model"].dropna().unique()
    )
    selected_rows = df_t[df_t["Model"] == model_name]

    if selected_rows.empty:
        st.warning("No rows found for selection.")
        st.stop()
    selected_row = selected_rows.iloc[0]

    folder = selected_row["Folder"]
    prompt_file = selected_row["Prompt File"]
    output_file = selected_row["Output File"]


#Resolve paths
model_folder = MODEL_MAP.get(model_name, model_name.lower().replace(" ", "_"))

prompt_path = PROMPT_DIR / folder / prompt_file
output_path = OUTPUT_DIR / folder / model_folder / output_file

prompt_content = read_text_file(prompt_path)
model_response = read_text_file(output_path)

#Header
st.subheader("Selected Evaluation")

if IS_NEW_FORMAT:
    cols = st.columns(5)
    labels = ["Doc Type", "Task", "Case", "Model", "Final Score"]
    values = [
        doc_type,
        task_id,
        str(case_id),
        model_name,
        f"{selected_row['case_final']:.2f}"
        if not pd.isna(selected_row.get("case_final")) else "-",
    ]
    for c, lab, val in zip(cols, labels, values):
        with c:
            st.markdown(f"**{lab}**")
            st.write(val)
else:
    cols = st.columns(4)
    labels = ["Failure Type", "Case", "Task", "Model"]
    values = [failure_type, case_name, task_name, model_name]
    for c, lab, val in zip(cols, labels, values):
        with c:
            st.markdown(f"**{lab}**")
            st.write(val)

st.divider()


# ============ 1. Item-Level Scoring ============
if IS_NEW_FORMAT:
    st.header("1. Item-Level Scoring")

    tags_str = selected_row.get("overall_tags", "")
    if pd.notna(tags_str) and str(tags_str).strip():
        tag_list = [t.strip() for t in str(tags_str).split(",") if t.strip()]
    else:
        tag_list = []

    c1, c2 = st.columns([1, 4])
    with c1:
        st.metric(
            "Final Score",
            f"{selected_row['case_final']:.2f}"
            if not pd.isna(selected_row.get("case_final")) else "-"
        )
    with c2:
        if tag_list:
            st.markdown("**Failure Tags**")
            for t in tag_list:
                st.markdown(f"- `{TAG_LABEL.get(t, t)}`")
        else:
            st.markdown("**Failure Tags**:None")

    display_df = selected_rows.copy()
    display_df["GT"] = display_df["gt_status"].map(STATUS_LABEL).fillna("-")
    display_df["Score"] = display_df["score"].map(score_label)
    display_df["Tag"] = display_df["failure_tag"].fillna("")

    show_cols = ["GT", "item", "gt_status", "field_value", "Score", "Tag", "gt_evidence"]
    show_cols = [c for c in show_cols if c in display_df.columns]

    st.dataframe(
        display_df[show_cols].rename(columns={
            "item": "Info Item",
            "gt_status": "GT Status",
            "field_value": "Model Answer",
            "gt_evidence": "Evidence",
        }),
        use_container_width=True,
        hide_index=True,
    )

else:
    st.header("1. Evaluation Result")
    result = selected_row["Result"]
    analysis = selected_row["Analysis"]

    c1, c2 = st.columns([1, 4])
    with c1:
        st.metric("Overall Result", result_icon(result))
    with c2:
        st.markdown("**Analysis**")
        st.write(analysis)

st.divider()

if IS_NEW_FORMAT:
    st.header("2. Ground Truth (This Task)")

    gt_file = GT_DIR / "gt_effective.json"
    if gt_file.exists():
        gt = json.loads(gt_file.read_text())
        gt_task = gt.get(doc_type, {}).get(task_id, {})

        if gt_task:
            gt_rows = []
            for item, val in gt_task.items():
                gt_rows.append({
                    "GT": STATUS_LABEL.get(val.get("status"), "-"),
                    "Info Item": item,
                    "Status": val.get("status"),
                    "Evidence": val.get("evidence") or "",
                })
            st.dataframe(
                pd.DataFrame(gt_rows),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info(f"No GT found for {doc_type} / {task_id}")
    else:
        st.info(f"GT file not found: {gt_file}")

    st.divider()

st.header("3. Rubric")
st.caption("Two atomic dimensions for scoring (v1.1).")

rubric_data = [
    {
        "Dimension": "D1: Unsupported Confirmation",
        "Question": "Does the model give a definite answer when the doc is Missing or Partial?",
        "Applies to": "GT = Missing / Partial",
    },
    {
        "Dimension": "D2: Evasion",
        "Question": "Does the model claim 'not specified' when the doc actually has the info?",
        "Applies to": "GT = Present",
    },
]
st.dataframe(pd.DataFrame(rubric_data), use_container_width=True, hide_index=True)

st.markdown("**Failure tags (v1.1)**")
st.markdown("""
- `UNSUPPORTED_CONFIRMATION` — D1, Missing field given definite content
- `VAGUE_NO_COMMIT` — D1, Missing field only says "I don't know"
- `OVERCLAIM` — D1, Partial field upgraded to definite
- `MISSED_GAP` — D1, Partial field treated as fully missing
- `EVASION` — D2, Present field claimed "not specified"
- `WRONG_ANSWER` — D2, Present field answered incorrectly
- `MISSING_FIELD` — model left the field empty
""")

st.divider()

st.header("4. Model Response")
with st.container(border=True):
    st.text(model_response)
st.divider()

st.header("5. Source Documents & Prompt")
with st.container(border=True):
    st.text(prompt_content)
st.divider()

st.header("6. Recorded Output Summary")

if IS_NEW_FORMAT and "model_output" in selected_row:
    recorded_output = selected_row["model_output"]
elif not IS_NEW_FORMAT and "Model Output" in selected_row:
    recorded_output = selected_row["Model Output"]
else:
    recorded_output = ""

with st.container(border=True):
    st.write(recorded_output)

with st.expander("File Information"):
    st.write("**Prompt file:**")
    st.code(str(prompt_path))
    st.write("**Model output file:**")
    st.code(str(output_path))
    st.write("**Scoring file:**")
    st.code(str(SCORING_FILE))