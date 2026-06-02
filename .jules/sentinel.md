## 2024-06-02 - Arbitrary Code Execution via eval() on Session State
**Vulnerability:** script.py was using Python's `eval()` to dynamically check validation state of Streamlit session variables like 'st.session_state.project' strings.
**Learning:** `eval()` is a security anti-pattern that can lead to arbitrary code execution, and evaluating string representations of dictionary-like properties is unsafe.
**Prevention:** Always use safe dictionary access methods like `st.session_state.get(key)` instead of `eval()` when dynamically resolving property names.
