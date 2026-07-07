## 2024-07-07 - Add loading feedback for AI operations
**Learning:** In Streamlit applications, long-running operations (like AI API calls and compilation) lack built-in loading states, leaving users unsure if an action is processing.
**Action:** Always wrap these operations in a `with st.spinner("..."):` block to provide immediate visual feedback.
