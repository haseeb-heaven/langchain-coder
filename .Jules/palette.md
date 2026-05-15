## 2024-05-13 - [Streamlit Feedback Patterns]
**Learning:** In Streamlit applications, long-running operations like AI generation should use `with st.spinner():` to provide immediate visual feedback.
**Action:** When implementing AI generation or API calls, wrap them in a spinner context manager.
