## 2026-07-03 - Added visual feedback for long-running operations
**Learning:** Users lack visibility during long-running operations like AI code generation or execution, leading to uncertainty about the app's state.
**Action:** Wrap such long-running operations (e.g., API calls, heavy computations) in a `with st.spinner("..."): ` block in Streamlit to provide immediate and clear visual feedback.
