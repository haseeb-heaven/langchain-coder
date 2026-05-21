## 2024-05-21 - Remove dangerous eval() checking Streamlit session state
**Vulnerability:** Found `eval()` being used to check if variables like `'st.session_state.project'` were set. This is a critical security anti-pattern that can lead to arbitrary code execution if any input gets into the evaluated string.
**Learning:** Never use `eval()` to dynamically evaluate code strings or check dictionary values, even for seemingly safe internal state checks.
**Prevention:** Use safer alternatives like `st.session_state.get(key)` directly with the actual dictionary keys.
