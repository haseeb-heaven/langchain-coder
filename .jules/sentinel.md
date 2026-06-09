## 2026-06-09 - Fix arbitrary code execution vulnerability via eval
**Vulnerability:** Arbitrary code execution vulnerability due to using `eval()` on string values to dynamically resolve variables.
**Learning:** Using `eval()` to dynamically check dictionary values or evaluate string inputs is a security anti-pattern that can lead to arbitrary code execution.
**Prevention:** Use safer alternatives like `dict.get(key)` or `st.session_state.get(key)`.
