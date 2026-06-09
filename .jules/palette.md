## 2026-06-09 - Streamlit Accessibility Context Loss
**Learning:** In Streamlit UI, inputs using `label_visibility='collapsed'` or `'hidden'` lose accessibility context for screen readers.
**Action:** Compensate by providing descriptive `help` tooltips and actionable `placeholder` examples to maintain a11y context.
