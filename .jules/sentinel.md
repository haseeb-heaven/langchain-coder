## 2026-07-25 - Remove Dangerous eval() Execution
**Vulnerability:** Arbitrary code execution vulnerability via the use of `eval()` to check if Streamlit session state variables were set in `script.py`.
**Learning:** Using `eval()` with any dynamically-referenced string is a major security anti-pattern as it executes arbitrary code.
**Prevention:** Use safer dictionary access methods like `st.session_state.get(key)` instead of evaluating code strings.
