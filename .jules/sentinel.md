## 2026-06-17 - Removed `eval()` anti-pattern in state checks
**Vulnerability:** Arbitrary code execution vulnerability via the use of `eval()` to check if Streamlit session state variables were set in `script.py`.
**Learning:** `eval()` should never be used to dynamically evaluate code strings or check dictionary values, as it's a security anti-pattern that can lead to arbitrary code execution if inputs are maliciously crafted.
**Prevention:** Instead of using `eval()`, use safer alternatives like `dict.get(key)` or `st.session_state.get(key)`.
