## 2026-08-23 - Remove eval() usage in Vertex AI checks
**Vulnerability:** Arbitrary Code Execution via eval()
**Learning:** Using eval() to dynamically check for Streamlit session state variables allows potential arbitrary code execution if the input is ever manipulated, and it's an insecure anti-pattern.
**Prevention:** Use safer alternatives like st.session_state.get(key) to retrieve session state values dynamically without evaluating strings as code.
