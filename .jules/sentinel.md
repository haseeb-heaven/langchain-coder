## 2026-08-08 - Prevent eval() Code Execution
**Vulnerability:** Use of eval() to dynamically check session state variables in script.py.
**Learning:** Using eval() for simple truthiness checks on variables is a dangerous anti-pattern that can lead to arbitrary code execution if inputs become user-controlled.
**Prevention:** Always use safe accessors like st.session_state.get(key) rather than executing strings.
