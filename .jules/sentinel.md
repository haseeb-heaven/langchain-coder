## 2026-06-26 - Prevent eval() in Session State Checks
**Vulnerability:** Use of eval() to dynamically check variable values (st.session_state).
**Learning:** Developers used eval() as a shortcut to evaluate hardcoded string variables. While not immediately exploitable via user input here, it establishes a dangerous pattern that can lead to arbitrary code execution if user input reaches the eval context.
**Prevention:** Never use eval() to check dictionary or session state values. Use safer alternatives like st.session_state.get(key).
