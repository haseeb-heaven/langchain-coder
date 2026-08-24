## 2026-08-24 - Prevent Arbitrary Code Execution using eval() in session state checks

**Vulnerability:** The application uses `eval()` to dynamically check if values like `st.session_state.project` exist. This is a critical security risk because it allows for arbitrary code execution if an attacker can control the string being evaluated.
**Learning:** Checking state values should never use `eval()`. Instead of passing string representations of variable access, we can safely access variables directly or safely use dictionary lookups using `.get()`.
**Prevention:** Always use safe dictionary lookup methods like `dict.get(key)` or direct property access instead of `eval()` to prevent command injection and arbitrary code execution vulnerabilities.
