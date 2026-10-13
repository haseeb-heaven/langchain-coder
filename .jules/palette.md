## 2026-06-26 - Accessibility context lost with hidden labels
**Learning:** In Streamlit UI, inputs using `label_visibility='collapsed'` or `'hidden'` lose accessibility context for screen readers.
**Action:** Compensate by providing descriptive `help` tooltips and actionable `placeholder` examples.
## 2026-10-13 - Adding Native Streamlit Tooltips
**Learning:** For Streamlit applications, utilizing the native `help` parameter in input widgets (like `st.selectbox` and `st.radio`) is a highly effective, low-risk micro-UX enhancement that improves accessibility and clarity without requiring custom CSS or complex layout changes.
**Action:** When working on Streamlit UIs, look for opportunities to add `help` text to configuration options or form inputs that may benefit from brief, in-context explanations to guide users.
