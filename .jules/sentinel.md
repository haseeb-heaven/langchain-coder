## 2026-07-13 - Remove Dangerous eval() for Session State
**Vulnerability:** Arbitrary Code Execution (CWE-94) via `eval()` usage on string representations of session state variables.
**Learning:** Never use `eval()` to check dictionary values or dynamically evaluate code strings, as it is a security anti-pattern that can lead to arbitrary code execution if inputs become user-controllable.
**Prevention:** Use safer alternatives like `dict.get(key)` or `st.session_state.get(key)` to retrieve values dynamically.
