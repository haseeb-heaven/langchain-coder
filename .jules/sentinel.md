## 2024-05-24 - Remove eval() for state variables
**Vulnerability:** Use of eval() to evaluate dynamic variable strings for st.session_state keys, which can lead to arbitrary code execution if inputs are not properly sanitized.
**Learning:** Using eval() to dynamically check session state is an insecure anti-pattern. While the inputs in this specific instance were hardcoded, it establishes a dangerous pattern that could be copied to areas with user-controlled input.
**Prevention:** Use dictionary lookups or safer alternatives like st.session_state.get(key) to check for variable existence and truthiness.
