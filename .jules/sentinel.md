## 2024-05-15 - Remove eval() for Session State Evaluation
**Vulnerability:** The `eval()` function was being used to dynamically evaluate dictionary keys representing `st.session_state` variables, potentially allowing arbitrary code execution.
**Learning:** Using `eval()` to dynamically check values from a string representation of state variables is a security anti-pattern.
**Prevention:** Never use `eval()` to check dictionary values. Use safer alternatives like `st.session_state.get(key)` to access session state directly.
