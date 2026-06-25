## 2026-06-25 - Removed unsafe eval() in script.py
**Vulnerability:** The application used `eval()` to check if variables in `st.session_state` were set, which could lead to arbitrary code execution if user input reaches those variables.
**Learning:** Using `eval()` to dynamically access dictionary or object properties is a dangerous anti-pattern.
**Prevention:** Always use safe access methods like `dict.get(key)` or `getattr(obj, key)` instead of dynamically evaluating code strings.
