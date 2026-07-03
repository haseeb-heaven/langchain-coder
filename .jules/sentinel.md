## 2026-07-03 - Remove eval() for state checks
**Vulnerability:** Arbitrary code execution risk from using eval() to check Streamlit session state variables.
**Learning:** Never use eval() to dynamically evaluate code strings or check dictionary values, as it is a security anti-pattern that can lead to arbitrary code execution if inputs can be manipulated.
**Prevention:** Instead, use safer alternatives like dict.get(key) or st.session_state.get(key).
