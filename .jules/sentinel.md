## 2026-07-22 - Remove eval() anti-pattern
**Vulnerability:** The application used eval() to dynamically evaluate string representations of session state keys.
**Learning:** Using eval() is a security anti-pattern that can lead to arbitrary code execution if inputs are not strictly controlled.
**Prevention:** Always use safe dictionary lookups like st.session_state.get(key) instead of evaluating code strings.
