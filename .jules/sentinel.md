## 2026-06-10 - Fix eval() vulnerability for state checking
**Vulnerability:** The code used `eval("st.session_state." + var_name)` or similar string evaluations to check if Streamlit session state properties were set.
**Learning:** Using `eval()` to dynamically evaluate code strings is a security anti-pattern that can lead to arbitrary code execution if the input is ever influenced by users.
**Prevention:** Use safer alternatives like `dict.get(key)` or `st.session_state.get(key)` for dynamic property access.
