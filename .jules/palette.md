## 2026-07-17 - [Streamlit Feedback Patterns]
**Learning:** In Streamlit applications, long-running operations like AI API calls or code execution block the UI without visual feedback. Wrapping wide multi-line conditional branches to add spinners exceeds micro-UX line constraints.
**Action:** Wrap long-running operations using `with st.spinner("..."):` on smaller, targeted execution blocks rather than large conditional branches to provide immediate feedback while keeping code diffs minimal.
