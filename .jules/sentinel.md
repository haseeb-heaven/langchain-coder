## 2026-06-23 - Remove insecure eval() for session state checking
**Vulnerability:** Arbitrary code execution risk from using eval() on dictionary keys to check Streamlit session state properties.
**Learning:** Using eval() to dynamically evaluate code strings or check dictionary values is a security anti-pattern that can lead to arbitrary code execution if inputs are not tightly controlled.
**Prevention:** Use safer alternatives like dict.get(key) or st.session_state.get(key) to securely access dynamic state variables.
