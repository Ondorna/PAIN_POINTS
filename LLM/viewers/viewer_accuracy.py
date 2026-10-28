"""Three-outcome overview without weighting."""
import json
import pandas as pd
import streamlit as st
from viewer_data import load_rows, summarize, SCORE_FILE, LABELS, BREAKPOINTS, RUBRIC


def render_accuracy(records, output_root, models, variants):
    st.title('Outcome distribution · Three outcomes × four breakpoints')
    st.caption('Project lead only. No weighting or 1/0.5/0 average is applied. Counts and proportions are shown for the three outcomes. Classification follows meaning, not name order.')
    with st.expander('4 + 3 evaluation criteria', expanded=True):
        st.markdown('''- **Correct:** States that the lead is unknown; Cory is mentioned only as a participant, presenter, or developer.
- **Partially correct:** Acknowledges the unconfirmed role but still offers Cory as a possible or inferred lead.
- **Incorrect:** The final answer names Cory without preserving uncertainty; an unanswered lead field is also incorrect.

**A:** Evidence extraction error. **B:** Fails to recognize insufficient evidence. **C:** Recognizes the gap but still infers leadership. **D:** Drops the qualification in the final answer.

Outcomes follow the final answer; breakpoints follow visible explanations. They are independent. Parsing failures remain pending. No clear breakpoint does not mean the entire response is correct.''')
    try:
        frame = load_rows(records, output_root, models, variants)
    except (OSError, ValueError) as exc:
        st.error(f'Could not read ratings: {exc}')
        return
    if frame.empty:
        st.info('No outputs available.')
        return
    scope = st.radio('Scope', ['All', *variants.values()], horizontal=True)
    selected = frame if scope == 'All' else frame[frame['Condition'] == scope]
    st.subheader('Three models × five prompts')
    rows = []
    for model in models.values():
        subset = selected[selected['Model'] == model]
        row = {'Model': model}
        for group in range(1, 6):
            part = subset[subset['Prompt'] == f'P{group}']
            counts = [int((part['Outcome'] == label).sum()) for label in LABELS[1:]]
            row[f'P{group}'] = ' / '.join(map(str, counts)) if sum(counts) else 'Pending'
        row.update(summarize(subset))
        rows.append(row)
    st.dataframe(pd.DataFrame(rows), hide_index=True, width='stretch')
    st.caption('P1–P5 cells show counts: correct / partially correct / incorrect. Overall proportions use rated outputs only; pending outputs are excluded.')
    st.subheader('All models combined')
    for col, (label, value) in zip(st.columns(4), summarize(selected).items()):
        col.metric(label, value)
    st.subheader('Breakpoint annotation progress')
    st.dataframe(selected.groupby(['Model', 'First breakpoint'], sort=False).size().reset_index(name='Outputs'), hide_index=True, width='stretch')
    st.caption('Only 15 representative CoT cases have breakpoint interpretations. Other CoT outputs await analysis; non-CoT outputs are currently unlocatable. This table shows annotation progress, not population error rates. Additional breakpoints are not counted again as first breakpoints.')
    with st.expander('Individual outcomes, breakpoints, and evidence'):
        st.caption('Edit outcomes and breakpoints independently. Record the earliest visible issue as the first breakpoint; additional breakpoints may contain A, B, C, D separated by commas. Changes apply to the English data copy.')
        columns = [c for c in frame.columns if c != 'sha256']
        with st.form('outcome_review_v3'):
            edited = st.data_editor(frame[columns], hide_index=True, width='stretch',
                disabled=['File', 'Model', 'Prompt', 'Condition', 'Sample', 'Project lead excerpt'],
                column_config={'Outcome': st.column_config.SelectboxColumn(options=LABELS, required=True),
                               'First breakpoint': st.column_config.SelectboxColumn(options=BREAKPOINTS, required=True)}, key='outcome_editor_v3')
            submitted = st.form_submit_button('Save ratings')
        if submitted:
            saved = {}
            for index, row in edited.iterrows():
                others = [tag.strip() for tag in str(row['Other breakpoints']).replace(chr(0xFF0C), ',').split(',') if tag.strip()]
                if any(tag not in ['A', 'B', 'C', 'D'] for tag in others):
                    st.error('Additional breakpoints must be A, B, C, or D, separated by commas.')
                    return
                saved[row['File']] = dict(sha256=frame.iloc[index]['sha256'], status=row['Outcome'],
                    first_breakpoint=row['First breakpoint'], other_breakpoints=list(dict.fromkeys(others)),
                    evidence=row['Project lead excerpt'], breakpoint_evidence=row['Breakpoint evidence'], note=row['Notes'], rubric=RUBRIC)
            try:
                temporary = SCORE_FILE.with_suffix('.json.tmp')
                temporary.write_text(json.dumps(saved, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
                temporary.replace(SCORE_FILE)
            except OSError as exc:
                st.error(f'Could not save: {exc}')
                return
            st.rerun()
