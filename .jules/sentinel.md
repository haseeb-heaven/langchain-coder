## 2026-07-02 - Remove eval() usage in session state checks
**Vulnerability:** Arbitrary code execution vulnerability due to the use of `eval()` to check if session state variables are set.
**Learning:** `eval()` should never be used to dynamically evaluate code strings or check dictionary values, as it is a security anti-pattern that can lead to arbitrary code execution if an attacker can manipulate the string being evaluated.
**Prevention:** Instead of `eval()`, use safer alternatives like `st.session_state.get(key)` to retrieve and check values from the session state dictionary.
