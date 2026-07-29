## 2026-07-29 - Remove Dangerous eval() in script.py
**Vulnerability:** The application was using the dangerous built-in `eval()` function to check if variables exist in `st.session_state`.
**Learning:** Checking state values via string evaluation is a severe anti-pattern that can lead to arbitrary code execution if user inputs can influence the evaluated string.
**Prevention:** Always use safe dictionary access methods like `st.session_state.get(key)` to retrieve and check values instead of dynamically evaluating strings.
