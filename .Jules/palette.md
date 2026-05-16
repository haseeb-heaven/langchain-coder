## 2024-05-19 - Added loading spinners for long-running AI operations
**Learning:** AI/API operations take time, causing a lag in responsiveness where users might wonder if their request was received. Wrapping these async operations with `st.spinner()` provides immediate feedback, keeping users engaged and informed that work is in progress.
**Action:** Use `st.spinner()` for all long-running asynchronous AI/API logic blocks in the Streamlit application.
