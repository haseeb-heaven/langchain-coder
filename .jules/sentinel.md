## 2026-08-10 - [Replace insecure eval() for accessing session state variables]
**Vulnerability:** Arbitrary code execution risk through eval() used to access Streamlit session state variables in script.py.
**Learning:** Using eval() to dynamically check for Streamlit session state variables is a severe security risk and bad practice, as it opens the door to arbitrary code execution.
**Prevention:** Always use safer alternatives like st.session_state.get(key) to retrieve session state variables instead of constructing strings and evaluating them.
