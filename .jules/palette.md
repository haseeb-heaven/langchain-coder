## 2026-06-19 - Enhance accessibility for collapsed labels in Streamlit inputs
**Learning:** In Streamlit UIs, inputs using `label_visibility='collapsed'` or `'hidden'` lose accessibility context for screen readers and general usability.
**Action:** Compensate by providing descriptive `help` tooltips and actionable `placeholder` examples for any hidden labels.
