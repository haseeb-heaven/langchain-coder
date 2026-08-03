
## 2026-08-03 - [eval() removal]
**Vulnerability:** Arbitrary Code Execution Risk via eval() in script.py
**Learning:** Using eval() to dynamically evaluate string representations of variable paths (like 'st.session_state.project') is an anti-pattern. It introduces security vulnerabilities since arbitrary code can be executed if input is tainted.
**Prevention:** Instead of evaluating strings, access dictionary or session state values directly using their keys and safe retrieval methods like st.session_state.get(key).
