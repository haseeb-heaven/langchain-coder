
## 2024-06-01 - [Context Loss in Streamlit Inputs]
**Learning:** When using Streamlit UI components like `st.text_input` and `st.text_area` with `label_visibility='hidden'` or `label_visibility='collapsed'`, screen readers and users lose critical context about what the field is for, significantly reducing accessibility.
**Action:** Always compensate for hidden labels by providing a descriptive `help` tooltip and actionable `placeholder` examples so that the purpose of the input remains clear.
