## 2026-06-26 - Accessibility context lost with hidden labels
**Learning:** In Streamlit UI, inputs using `label_visibility='collapsed'` or `'hidden'` lose accessibility context for screen readers.
**Action:** Compensate by providing descriptive `help` tooltips and actionable `placeholder` examples.
## 2026-10-09 - Adding Tooltips to Streamlit Native Widgets
**Learning:** Adding the `help` parameter to standard Streamlit components like `st.selectbox` and `st.radio` provides a built-in, accessible tooltip functionality out of the box, allowing for rapid micro-UX enhancements that don't clutter the interface.
**Action:** When working on Streamlit apps, always consider utilizing the `help` parameter to improve form controls' context instead of adding separate text descriptions.
