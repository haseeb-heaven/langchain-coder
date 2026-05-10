## 2024-05-10 - Streamlit Interactive State Spinners
**Learning:** In Streamlit, because the entire app reruns on interactions like button clicks, long-running processes (like AI code generation or API calls) create a frozen UI state if unhandled. It is critical to provide visual feedback immediately for these operations, otherwise the user believes the app is broken.
**Action:** Always wrap operations on `st.form_submit_button` or `st.button` actions that perform network or AI calls with `with st.spinner("Doing work..."):`. This gives an immediate responsive feel for latency-prone features.
