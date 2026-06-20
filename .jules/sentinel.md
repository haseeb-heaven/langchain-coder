## 2024-06-20 - Insecure use of eval() for state keys
**Vulnerability:** The application used `eval()` to dynamically evaluate state keys like `'st.session_state.project'` from a dictionary.
**Learning:** Using `eval()` to evaluate state keys is a security anti-pattern. It can lead to arbitrary code execution if inputs are user-controlled.
**Prevention:** Never use `eval()` to dynamically check variables or keys. Always use safer alternatives like `st.session_state.get(key)`.
