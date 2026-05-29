## 2024-05-29 - [CRITICAL] Prevent Arbitrary Code Execution Risk in UI state checks
**Vulnerability:** The Streamlit application used `eval(var)` to check the status of session state variables, which opens the possibility of arbitrary code execution if user inputs or state somehow influence the variables evaluated.
**Learning:** `eval()` should never be used to dynamically evaluate dictionary values or application states.
**Prevention:** Use safer alternatives like `dict.get(key)` or `st.session_state.get(key)` to safely retrieve and verify variable states.
