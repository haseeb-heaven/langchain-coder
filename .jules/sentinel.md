## 2026-07-24 - Remove eval() for Session State Evaluation
**Vulnerability:** The application used `eval()` to dynamically evaluate string literals (e.g., `'st.session_state.project'`) from dictionary keys.
**Learning:** While the strings were hardcoded, using `eval()` to check state is a security anti-pattern. If any dynamically generated or user-controlled string entered this flow, it would lead to Critical Arbitrary Code Execution.
**Prevention:** Never use `eval()` to dynamically evaluate code strings or check dictionary values. Instead, use safe retrieval methods like `st.session_state.get(key)`.
