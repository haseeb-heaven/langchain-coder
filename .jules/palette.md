## 2026-07-26 - Adding Immediate Visual Feedback for Async Operations
**Learning:** In Streamlit applications, complex synchronous or long-running operations (like LLM API calls or code execution) cause the UI to appear frozen unless explicit loading states are provided. Users benefit greatly from immediate visual feedback.
**Action:** Use `st.spinner()` as a wrapper around targeted, smaller execution blocks (e.g., API calls) instead of large conditional branches to provide clean loading states while keeping code changes minimal.
