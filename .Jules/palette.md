## 2024-05-21 - Streamlit Inputs Missing Accessibility Context
**Learning:** When using `label_visibility='collapsed'` in Streamlit, the label is completely removed from the DOM, causing the input to lose accessibility context for screen readers.
**Action:** Always provide descriptive `help` tooltips and actionable `placeholder` examples for collapsed inputs to restore accessibility context.
