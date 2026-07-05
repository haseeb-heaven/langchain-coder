## 2026-07-05 - Remove eval() security anti-pattern
**Vulnerability:** Use of `eval()` to check dictionary values in `script.py` (lines 164-171).
**Learning:** Using `eval()` to evaluate strings is a security anti-pattern that can lead to arbitrary code execution if the input is ever derived from an untrusted source.
**Prevention:** Avoid `eval()` completely for dynamic property access. Use safer alternatives like `st.session_state.get(key)`.
