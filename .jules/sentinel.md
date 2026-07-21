## 2026-07-21 - [CRITICAL] Remove eval() usage from session state check
**Vulnerability:** Arbitrary Code Execution (CWE-94) via eval() when checking if st.session_state items exist.
**Learning:** Checking state values with eval(var_name_string) is extremely dangerous and can lead to arbitrary code execution if user inputs can somehow manipulate these values or variable names.
**Prevention:** Never use eval() to dynamically evaluate code strings or check dictionary values. Instead, use safe lookups like st.session_state.get(key).
