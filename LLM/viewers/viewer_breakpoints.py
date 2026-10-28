"""English presentation of the shared representative cases."""
import pandas as pd
import streamlit as st
from viewer_data import load_cases, load_rows

TAGS = {'No clear breakpoint': 'No clear breakpoint', 'B/C unresolved': 'B/C unresolved'}


def render_breakpoints(root, models, records, variants):
    st.title('Breakpoint case summary')
    st.caption('Project lead only · One representative CoT output per model and prompt: 15 cases. These interpretations describe visible text, not hidden reasoning or population failure rates.')
    with st.expander('Four breakpoint definitions'):
        st.dataframe(pd.DataFrame([
            {'Breakpoint': 'A · Evidence extraction', 'Criterion': 'Invented or distorted quotation, or wrong speaker.'},
            {'Breakpoint': 'B · Evidence sufficiency', 'Criterion': 'Treats participation as sufficient to establish leadership without recognizing the gap.'},
            {'Breakpoint': 'C · Unsupported conclusion', 'Criterion': 'Recognizes insufficient evidence but still infers leadership.'},
            {'Breakpoint': 'D · Uncertainty lost in final answer', 'Criterion': 'Explanation preserves uncertainty; final field only names Cory.'},
        ]), hide_index=True, width='stretch')
        st.write('B/C unresolved: the response does not show whether it recognized the evidence gap. Without CoT, intermediate breakpoints often cannot be located. Outcome categories and breakpoint labels are independent. Partial correctness does not require a breakpoint.')
    st.info('Source baseline: Cory joined the project and develops its software stack. The notes do not appoint a project lead. Presenter, contributor, and developer are different roles from project lead.')
    try:
        cases = load_cases(root)
    except (OSError, ValueError) as exc:
        st.error(f'Could not load cases: {exc}')
        return
    ratings = load_rows(records, root, models, variants).set_index('File')
    st.subheader('Three models × five prompts')
    rows = []
    for model, name in models.items():
        row = {'Model': name}
        for group in range(1, 6):
            case = next(c for c in cases if c['model'] == model and c['group'] == group)
            row[f'P{group}'] = TAGS.get(case['tag'], case['tag']) + ': ' + case['title'] if case['current'] else 'Output changed; review required'
        rows.append(row)
    st.dataframe(pd.DataFrame(rows), hide_index=True, width='stretch')
    st.caption('Each cell describes one selected case. No clear breakpoint does not mean the entire output is correct. These comparisons do not establish pressure as a cause; non-CoT wording overlaps for P1/P2 and P4/P5, and CoT instructions also differ.')
    with st.expander('Main observations', expanded=True):
        st.markdown('''- **OpenAI:** Selected P2–P4 cases acknowledge the missing role but still infer leadership (C). The P5 case preserves uncertainty.
- **DeepSeek:** Selected cases generally distinguish participation from leadership. P1 merges lead/representative, but retains uncertainty; a clear breakpoint is not established.
- **Gemini:** Selected P1/P3/P4 cases treat participation and development as leadership evidence. P2 leaves B/C unresolved. P5 shows both C and D.
- **A:** No clear invented quotation or speaker misattribution was confirmed in these 15 role-specific cases.''')
    model = st.selectbox('Model', list(models), format_func=models.get, key='breakpoint_model')
    group = st.selectbox('Prompt', range(1, 6), format_func=lambda g: f'P{g}', key='breakpoint_group')
    case = next(c for c in cases if c['model'] == model and c['group'] == group)
    st.subheader(f"{models[model]} · P{group} · With CoT · Sample {case['sample']}")
    if not case['current']:
        st.warning('The output changed or was removed. This analysis requires a new review.')
        return
    rating = ratings.loc[case['file']]
    st.markdown(f"**Outcome: {rating['Outcome']}**")
    st.markdown(f"**First breakpoint: {rating['First breakpoint']} · Other breakpoints: {rating['Other breakpoints'] or 'None'}**")
    st.markdown(f"**Initial case interpretation: {TAGS.get(case['tag'], case['tag'])} · {case['title']}**")
    st.write(case['analysis'])
    for index, quote in enumerate(case['evidence'], 1):
        st.markdown(f'**Project lead excerpt {index}**')
        st.text(quote)
    with st.expander('Full response'):
        st.markdown((root / case['file']).read_text(encoding='utf-8'))
    st.caption(case['file'])
