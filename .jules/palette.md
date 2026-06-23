## 2026-06-23 - Accessibility Context in Streamlit
**Learning:** In Streamlit applications, when inputs use label_visibility='collapsed' or 'hidden' (to save space or for aesthetic reasons), the input fields lose their accessibility context for screen readers and can become confusing for all users.
**Action:** Compensate for hidden labels by always providing descriptive `help` tooltips and actionable `placeholder` examples to maintain context and accessibility.
