## 2026-08-17 - Remove eval() for Session State
**Vulnerability:** The codebase uses `eval()` to dynamically check variables like `st.session_state.project`, which is an arbitrary code execution vulnerability risk.
**Learning:** Avoid using `eval()` to dynamically check for Streamlit session state variables.
**Prevention:** Always use safer alternatives like `st.session_state.get(key)` to prevent potential arbitrary code execution vulnerabilities.
