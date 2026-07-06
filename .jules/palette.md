## 2024-05-31 - Add visual feedback for long-running AI operations
**Learning:** In Streamlit applications, long-running operations (such as AI generation or API calls) can cause the UI to appear unresponsive, leading to poor user experience.
**Action:** Wrap long-running operations in a `with st.spinner("...");` block to provide clear, immediate visual feedback to the user.
