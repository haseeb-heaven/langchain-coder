## 2026-08-21 - [eval() Arbitrary Code Execution Risk in Streamlit]
**Vulnerability:** The use of `eval()` to check Streamlit session state variables (e.g. `eval('st.session_state.project')`).
**Learning:** Using `eval()` poses a significant arbitrary code execution vulnerability risk if the strings passed to it are ever influenced by user input. In this case, while checking internal state variables, relying on `eval()` is a dangerous pattern.
**Prevention:** Always use safe dictionary access methods like `st.session_state.get(key)` to check for variables dynamically, and explicitly avoid `eval()` for state inspection.
