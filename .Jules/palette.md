## 2024-05-14 - Accessibility for Collapsed Labels in Streamlit
**Learning:** In Streamlit UI, inputs using `label_visibility='collapsed'` or `hidden` lose accessibility context for screen readers and keyboard users.
**Action:** Always compensate by providing descriptive `help` tooltips and actionable `placeholder` examples for inputs where labels are visually hidden.
