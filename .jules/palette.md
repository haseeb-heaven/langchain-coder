## 2024-05-14 - Streamlit Inputs with Hidden Labels
**Learning:** In Streamlit, setting `label_visibility='collapsed'` or `'hidden'` on inputs (`st.text_input`, `st.text_area`) causes screen readers and users to lose context about what the input is for.
**Action:** When hiding labels for layout reasons, always compensate by providing a descriptive `help` tooltip and an actionable `placeholder` with an example.
