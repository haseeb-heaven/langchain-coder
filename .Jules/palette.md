## 2026-05-17 - Adding loading states to long-running Streamlit operations
**Learning:** Streamlit applications require explicit loading states (like `st.spinner`) for long-running operations (such as AI generation or API calls) to provide clear, immediate visual feedback and prevent users from thinking the application has frozen.
**Action:** Wrap long-running operations in `with st.spinner('...'):` blocks in Streamlit applications.
