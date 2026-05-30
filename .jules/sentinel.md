
## 2024-05-14 - Removed critical eval() vulnerability
**Vulnerability:** Use of `eval()` on string representations of variables (`'st.session_state.project'`) to dynamically check state values.
**Learning:** `eval()` should never be used to check state keys or variable values dynamically as it can lead to arbitrary code execution if the input is ever tainted, and it's generally a severe anti-pattern in Python.
**Prevention:** Use safe dictionary or state access patterns like `st.session_state.get(key)` instead of dynamically evaluating strings.
