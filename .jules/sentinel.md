## 2026-07-18 - Remove eval() usage in Streamlit app
**Vulnerability:** The `eval()` function is used in `script.py` to dynamically evaluate strings representing Streamlit session state variables (e.g., `'st.session_state.project'`).
**Learning:** Using `eval()` on strings is a security anti-pattern as it can lead to arbitrary code execution if the input strings are ever influenced by user input, and it's unnecessary here since we can access the session state dictionary directly.
**Prevention:** Always access `st.session_state` values using dictionary keys or attribute access (e.g., `st.session_state.get(key)`) instead of dynamically evaluating strings.
