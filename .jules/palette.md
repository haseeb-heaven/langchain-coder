## 2026-07-14 - Adding Spinners for AI Operations
**Learning:** Long-running LLM and execution API calls in Streamlit cause the UI to freeze without feedback, making users think the app crashed.
**Action:** Wrap long-running operations (like `fix_generated_code`, `convert_generated_code`, and `execute_code`) in a `with st.spinner("..."):` block to provide immediate visual feedback.
