## 2026-06-29 - Adding loading states to async operations
**Learning:** Long-running operations in Streamlit (like AI code generation, debugging, converting, and execution) cause the app to appear frozen without visual feedback, which is a poor user experience.
**Action:** Always wrap these long-running operations in a `with st.spinner("..."): ` block to provide immediate visual feedback to the user and improve perceived performance.
