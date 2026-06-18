## 2026-06-18 - Added accessibility tooltips to Streamlit inputs

**Learning:** When using `label_visibility='collapsed'` or `'hidden'` in Streamlit, the inputs lose their accessibility context for screen readers.
**Action:** Always provide descriptive `help` tooltips and actionable `placeholder` examples to compensate for the hidden labels and maintain accessibility.
