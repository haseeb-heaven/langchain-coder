
## 2026-07-16 - Remove eval() for Session State Access
**Vulnerability:** Arbitrary code execution via eval() used to access st.session_state variables.
**Learning:** Using eval() to dynamically evaluate state keys is a severe security risk and anti-pattern.
**Prevention:** Always use safe dictionary access methods like st.session_state.get(key) instead of eval().
