## 2024-05-16 - Avoid eval() for dynamic state access
**Vulnerability:** Arbitrary Code Execution via `eval()`.
**Learning:** Using `eval()` to dynamically access variables (like `eval('st.session_state.project')`) is a major security risk that can lead to arbitrary code execution if user inputs ever reach that evaluation context.
**Prevention:** Never use `eval()`. Use safe dictionary-like access methods such as `st.session_state.get(key)` instead.
