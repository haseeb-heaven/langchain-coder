## 2026-06-15 - Hidden/Collapsed Label Accessibility in Streamlit
**Learning:** In Streamlit UI, inputs using `label_visibility='collapsed'` or `'hidden'` lose accessibility context, making them difficult for screen reader users to understand.
**Action:** Always compensate by providing descriptive `help` tooltips and actionable `placeholder` examples to restore context.
