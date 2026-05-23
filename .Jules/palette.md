## 2024-05-23 - Accessibility of Streamlit Collapsed Labels
**Learning:** In Streamlit UI, inputs using `label_visibility='collapsed'` lose accessibility context because screen readers and users cannot see the label.
**Action:** Compensate by providing descriptive `help` tooltips and actionable `placeholder` examples for all inputs with collapsed labels.
