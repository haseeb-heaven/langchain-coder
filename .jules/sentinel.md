## 2026-09-19 - Prevent Arbitrary Code Execution via eval()
**Vulnerability:** The application used `eval()` to dynamically check if Streamlit session state variables were set, posing an arbitrary code execution risk.
**Learning:** Using `eval()` to evaluate strings of variable names is highly insecure, as malicious input could be executed.
**Prevention:** Always use safe dictionary access methods like `.get()` (e.g., `st.session_state.get(key)`) instead of evaluating strings representing variables.
