## 2026-07-15 - Remove eval() for session state checking
**Vulnerability:** Arbitrary code execution risk through eval() being used to dynamically resolve session state variables.
**Learning:** eval() was used as a shortcut to dynamically evaluate string variable names instead of directly accessing the dictionary state.
**Prevention:** Always use safe dictionary access methods like st.session_state.get(key) instead of eval() to retrieve dynamic variable values.
