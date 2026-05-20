## 2023-10-25 - Improve Streamlit inputs with tooltips and actionable placeholders
**Learning:** Streamlit inputs with `label_visibility='collapsed'` lose their primary accessibility context. Using repeated names as placeholders (e.g., "Input (Stdin)") provides little UX value and doesn't clarify intent.
**Action:** Always add descriptive `help` tooltips and actionable `placeholder` text (e.g., "e.g., Fix the index out of bounds error") for Streamlit inputs, especially when labels are collapsed, to ensure clear user guidance and better accessibility.
