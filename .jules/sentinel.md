## 2024-05-25 - Insecure eval() Usage

**Vulnerability:** Found insecure use of `eval()` in `script.py` when validating Streamlit session state variables.
**Learning:** Using `eval()` to dynamically check variable truthiness from string dictionary keys is a critical anti-pattern that can lead to arbitrary code execution if the input is ever controlled or influenced by external sources.
**Prevention:** Use safer alternatives like direct variable access or `st.session_state.get(key)` instead of `eval()` to dynamically access session state or object properties.
