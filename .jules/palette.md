## 2026-06-26 - Accessibility context lost with hidden labels
**Learning:** In Streamlit UI, inputs using `label_visibility='collapsed'` or `'hidden'` lose accessibility context for screen readers.
**Action:** Compensate by providing descriptive `help` tooltips and actionable `placeholder` examples.
## 2026-10-23 - Native Tooltips in Streamlit
**Learning:** Native tooltips in Streamlit can be easily added using the `help` parameter on input elements like `st.selectbox`, `st.radio`, and `st.checkbox`.
**Action:** Use the `help` parameter to add non-intrusive micro-UX improvements to Streamlit applications.
