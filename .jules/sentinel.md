## 2026-06-07 - Avoid eval() for dynamic state access
**Vulnerability:** Use of `eval()` to dynamically check values in dictionaries or `st.session_state` (found in `script.py` checking Vertex AI settings).
**Learning:** Even with hardcoded keys, using `eval()` is a critical security anti-pattern that can inadvertently lead to arbitrary code execution if keys are ever refactored to include user input.
**Prevention:** Always use safe dictionary access methods like `st.session_state.get(key)` instead of `eval()`.
