## 2026-06-16 - eval() State Checking Pattern
**Vulnerability:** Use of eval() to dynamically evaluate code strings for checking session state values in script.py.
**Learning:** Checking state by dynamically evaluating strings introduces a severe arbitrary code execution risk if those strings ever become influenced by user input.
**Prevention:** Never use eval() to dynamically evaluate code strings or check dictionary values. Always use safer alternatives like st.session_state.get(key).
