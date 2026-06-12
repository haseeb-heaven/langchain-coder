## 2024-05-18 - Streamlit Hidden Labels Accessibility
**Learning:** In Streamlit, inputs that use `label_visibility='collapsed'` or `'hidden'` lose their accessibility context for screen readers.
**Action:** Compensate for hidden/collapsed labels by providing descriptive `help` tooltips and actionable `placeholder` examples so that screen readers and visually impaired users can still understand the input's purpose.
