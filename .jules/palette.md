## 2024-06-25 - Improve accessibility of hidden and collapsed labels in Streamlit
**Learning:** In Streamlit UI, inputs using `label_visibility='collapsed'` or `'hidden'` lose accessibility context because screen readers lack the label text.
**Action:** Compensate for hidden/collapsed labels by consistently providing descriptive `help` tooltips and actionable `placeholder` examples so context is retained.
