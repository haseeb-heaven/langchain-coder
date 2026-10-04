## 2026-10-02 - Arbitrary Code Execution via eval()
**Vulnerability:** The `script.py` file dynamically checks Streamlit session state variables using `eval(var)` inside a list comprehension. This is a critical security vulnerability as it can lead to arbitrary code execution if `var` can be influenced by an attacker, and it's generally an unsafe pattern for accessing state.
**Learning:** Using `eval()` to dynamically access dictionary or object keys is a dangerous anti-pattern that exposes the application to arbitrary code execution.
**Prevention:** Avoid using `eval()` to dynamically check for variables. Always use safer alternatives like direct dictionary access or `get()` (e.g., `st.session_state.get(key)`) to prevent potential arbitrary code execution vulnerabilities.
