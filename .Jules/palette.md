## 2024-05-30 - Accessible Hidden Labels in Streamlit
**Learning:** When using `label_visibility='collapsed'` or `'hidden'` in Streamlit, inputs lose accessibility context for screen readers because the label is removed from the DOM.
**Action:** Always provide descriptive `help` tooltips and/or actionable `placeholder` text as a fallback to maintain accessibility when visual labels are hidden.
