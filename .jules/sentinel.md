## 2026-07-19 - Remove eval() to prevent arbitrary code execution
**Vulnerability:** The `eval()` function was used to dynamically evaluate strings from a dictionary mapping session state variables (`eval(var)`). While the current inputs were static strings, using `eval()` is a dangerous anti-pattern that can lead to arbitrary code execution if user inputs ever reach that code path.
**Learning:** Never use `eval()` to check or access dictionary values or object properties, as it executes the string as Python code, creating severe security risks.
**Prevention:** Use safer alternatives like direct dictionary lookups (e.g., `dict.get(key)` or `st.session_state.get(key)`) to access values dynamically without executing code.
