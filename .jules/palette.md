## 2026-06-06 - Streamlit Label Visibility Accessibility
**Learning:** When using `label_visibility='collapsed'` or `'hidden'` in Streamlit inputs, the input loses its accessibility context for screen readers and visual context for users.
**Action:** Compensate for hidden labels by always providing descriptive `help` tooltips and actionable `placeholder` examples to ensure accessibility and usability.
