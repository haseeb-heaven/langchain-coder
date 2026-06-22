## 2026-06-22 - Fix eval() anti-pattern for session state checking
**Vulnerability:** Code used `eval()` to dynamically check values in Streamlit's `session_state` based on string keys, which is a known anti-pattern that can lead to Remote Code Execution (RCE) if keys are ever user-controlled.
**Learning:** Even if the strings are currently hardcoded, using `eval()` to resolve object properties or dictionary items is a dangerous habit that breaks the "Trust nothing" principle.
**Prevention:** Always use safe dictionary access methods like `dict.get(key)` or `st.session_state.get(key)` instead of dynamically evaluating strings.
