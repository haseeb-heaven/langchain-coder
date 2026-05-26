## 2024-05-24 - Remove eval for state variable checks
**Vulnerability:** Use of `eval()` to dynamically check dictionary/state values.
**Learning:** Even with hardcoded keys, using `eval()` for state checks is a security anti-pattern that can lead to arbitrary code execution if the keys are ever refactored to use user input.
**Prevention:** Always use `st.session_state.get(key)` or `dict.get(key)` for dynamic state/dictionary lookups.
