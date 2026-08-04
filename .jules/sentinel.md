## 2026-08-04 - Insecure eval() usage for dictionary values
**Vulnerability:** The application used eval() to dynamically check state variables inside a list comprehension, which is a critical security anti-pattern.
**Learning:** Using eval() on code strings, even if seemingly controlled, introduces arbitrary code execution risks.
**Prevention:** Use safer alternatives such as dict.get(key) or st.session_state.get(key) for dynamic state evaluation.
