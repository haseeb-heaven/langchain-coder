
## 2024-05-25 - Improve accessibility of hidden Streamlit labels
**Learning:** In Streamlit UIs, using `label_visibility='collapsed'` or `hidden` causes elements to lose accessibility context for screen readers.
**Action:** Always provide descriptive `help` tooltips and actionable `placeholder` examples for inputs that have their labels hidden or collapsed to maintain accessibility and user context.
