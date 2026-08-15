## 2026-08-15 - [Fix Arbitrary Code Execution]
**Vulnerability:** Arbitrary Code Execution via eval() on session state variables.
**Learning:** Using eval() to dynamically check variables in Streamlit is highly insecure and can lead to arbitrary code execution if user input is ever involved.
**Prevention:** Always use st.session_state.get() to safely retrieve session state variables instead of dynamically evaluating strings.
