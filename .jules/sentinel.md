## 2026-06-29 - Removed eval() usage for variable checking
**Vulnerability:** Arbitrary code execution risk via eval() used to check dictionary keys.
**Learning:** Using eval() to check dynamic dictionary keys or session state variables is an anti-pattern.
**Prevention:** Always use safe dictionary access methods like dict.get(key) or st.session_state.get(key).
