## 2024-06-04 - Fix eval() vulnerability in Streamlit session state check
**Vulnerability:** Arbitrary Code Execution (ACE) via `eval()` used to dynamically evaluate `st.session_state` variable names.
**Learning:** Using `eval()` to resolve variable names dynamically is a critical security anti-pattern that can lead to remote code execution. It was used here to check if multiple Streamlit session state variables were set.
**Prevention:** Never use `eval()` to dynamically evaluate code strings or check dictionary values. Instead, use safer alternatives like `dict.get(key)` or `st.session_state.get(key)`.
