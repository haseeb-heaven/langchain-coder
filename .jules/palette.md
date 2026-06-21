## 2026-06-21 - Compensating for Collapsed Labels in Streamlit
**Learning:** Using `label_visibility='collapsed'` or `'hidden'` in Streamlit inputs removes the label from screen readers, causing a loss of accessibility context.
**Action:** Always provide descriptive `help` tooltips and actionable `placeholder` examples when hiding labels to ensure screen readers and visually impaired users still understand the input's purpose.
