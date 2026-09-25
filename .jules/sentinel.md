## 2026-09-25 - [Arbitrary Code Execution via eval()]
**Vulnerability:** The application uses `eval()` to dynamically check if certain Streamlit session state variables are set. While the variables are currently hardcoded, `eval()` introduces an arbitrary code execution risk if variable names were to become dynamically generated or user-controlled.
**Learning:** Checking state dynamically with `eval()` in Python is unsafe.
**Prevention:** Avoid using `eval()` to dynamically check for Streamlit session state variables. Always use safer alternatives like `st.session_state.get(key)` to safely access dynamically named properties.
