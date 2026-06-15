## 2026-06-15 - Remove eval() for Session State Checks
**Vulnerability:** The codebase was using `eval()` to evaluate variable strings like 'st.session_state.project' to check if they were set. This is a critical security anti-pattern that can lead to arbitrary code execution if the input is ever manipulated or dynamically generated.
**Learning:** Checking dictionary or session state values should never rely on dynamic string evaluation. `eval()` evaluates the expression in the current scope, opening up execution vectors.
**Prevention:** Instead of evaluating the full string 'st.session_state.key', store only the keys (e.g., 'project') and safely retrieve them using `st.session_state.get(key)`.
