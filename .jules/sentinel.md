## 2026-08-12 - [Fix eval() usage for Session State Checks]
**Vulnerability:** The code used `eval(var)` to dynamically evaluate string representations of Streamlit session state variables (like `'st.session_state.project'`).
**Learning:** Using `eval()` is a critical security risk as it can lead to arbitrary code execution if user inputs or dynamically generated strings are ever introduced into the evaluation target.
**Prevention:** Always use safe dictionary access methods like `st.session_state.get(key)` to retrieve values dynamically, avoiding code evaluation functions entirely.
