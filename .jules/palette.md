## 2026-07-12 - Adding Spinners for Long-Running Tasks
**Learning:** Long-running operations like AI code generation or API calls lack immediate visual feedback, leading to user confusion about whether the system is working.
**Action:** Always wrap long-running operations in Streamlit (like API calls or executions) with `with st.spinner("...");` to provide immediate, clear feedback. Apply this targetedly to avoid massive indentation changes.
