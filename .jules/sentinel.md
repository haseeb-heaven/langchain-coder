## 2026-07-20 - Remove eval() for Session State Checks
**Vulnerability:** Using `eval()` to evaluate variable names dynamically from `st.session_state`.
**Learning:** Using `eval()` is a critical security vulnerability as it allows arbitrary code execution if user input ever makes its way into the evaluated strings.
**Prevention:** Use `st.session_state.get(key)` directly with the keys rather than passing string representations of variable access to `eval()`.
