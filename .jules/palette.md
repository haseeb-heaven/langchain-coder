## 2026-06-24 - Compensate for hidden labels in Streamlit
**Learning:** In Streamlit applications, using `label_visibility='collapsed'` or `'hidden'` removes important context for screen readers and users.
**Action:** Always compensate for hidden labels by providing descriptive `help` tooltips and actionable `placeholder` examples.
