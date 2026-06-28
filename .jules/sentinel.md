## 2026-06-28 - Avoid using eval() for checking dictionary values
**Vulnerability:** Found eval() being used to dynamically evaluate variable names represented as strings, which can lead to arbitrary code execution.
**Learning:** eval() should never be used to check dictionary values or session state values dynamically, as it evaluates strings as Python code.
**Prevention:** Use safer alternatives like dict.get(key) or st.session_state.get(key) to access values dynamically without evaluating strings.
