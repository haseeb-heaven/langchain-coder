## 2026-08-13 - Remove insecure eval() for session state check
**Vulnerability:** Arbitrary code execution vulnerability (eval() used to check session state).
**Learning:** Using eval() to dynamically check variables is a major security risk. The original code used eval() on string representations of variables, which is unsafe.
**Prevention:** Use safe dictionary lookups like st.session_state.get(key) instead of eval() to verify application state safely.
