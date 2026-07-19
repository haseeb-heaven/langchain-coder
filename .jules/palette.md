## 2026-07-19 - Wrap long-running tasks in spinners
**Learning:** In Streamlit applications, long-running operations like AI generation, compilation, and execution can cause the UI to appear unresponsive, making users unsure if their click was registered.
**Action:** Wrap such long-running operations in `with st.spinner("..."): ` blocks to provide clear, immediate visual feedback to the user without disrupting the page structure or exceeding 50 lines of changed code.
