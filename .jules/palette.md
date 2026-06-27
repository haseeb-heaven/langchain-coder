## 2026-06-27 - Compensating for Collapsed Labels in Streamlit
**Learning:** In Streamlit UIs, using `label_visibility='collapsed'` or `'hidden'` removes the accessibility context for inputs.
**Action:** Compensate by providing descriptive `help` tooltips and actionable `placeholder` examples for these inputs to ensure users and screen readers understand their purpose.
## 2026-06-27 - Adding loading feedback for long-running operations in Streamlit
**Learning:** Long-running AI operations (generate, debug, convert, execute) cause the UI to freeze without visual feedback, leading to poor UX.
**Action:** Use `with st.spinner("Action name..."): ` wrappers around these long-running calls to provide immediate visual feedback.
