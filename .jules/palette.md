## 2026-06-26 - Accessibility context lost with hidden labels
**Learning:** In Streamlit UI, inputs using `label_visibility='collapsed'` or `'hidden'` lose accessibility context for screen readers.
**Action:** Compensate by providing descriptive `help` tooltips and actionable `placeholder` examples.
## 2026-10-24 - Adding Streamlit Tooltips
**Learning:** Native Streamlit components (like `st.selectbox`, `st.radio`, `st.checkbox`) support a built-in `help` parameter that automatically renders accessible tooltips. This is a clean, standard way to provide contextual guidance without cluttering the UI.
**Action:** Always utilize the `help` parameter on Streamlit input widgets to improve form clarity and micro-UX.
