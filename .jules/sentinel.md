## 2026-06-05 - Removed eval() usage
**Vulnerability:** Arbitrary code execution via `eval()`.
**Learning:** Never use `eval()` to dynamically evaluate code strings or check dictionary values. It is a security anti-pattern.
**Prevention:** Instead, use safer alternatives like `dict.get(key)` or `st.session_state.get(key)`.
