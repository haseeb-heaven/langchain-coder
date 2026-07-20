## 2026-07-20 - Wrap long-running operations in spinners
**Learning:** Long-running AI operations and system executions without visual feedback leave users wondering if the app has frozen.
**Action:** Always wrap these targeted execution blocks (like debugging, converting, executing) in `with st.spinner(...):` to provide immediate reassurance, while keeping diffs under 50 lines by wrapping smaller targeted blocks instead of large multi-line branches.
