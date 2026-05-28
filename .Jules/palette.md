## 2024-05-24 - Missing accessibility context for inputs with hidden labels
**Learning:** In Streamlit UI, inputs using `label_visibility='collapsed'` or `'hidden'` lose accessibility context for screen readers.
**Action:** Compensate by providing descriptive `help` tooltips and actionable `placeholder` examples to these inputs to restore the missing context.
