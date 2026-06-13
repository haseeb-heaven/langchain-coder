## 2026-06-13 - Unsafe eval() for session state keys
**Vulnerability:** Found `eval(var)` being used to dynamically check variables like 'st.session_state.project' within a list comprehension.
**Learning:** Using `eval()` even for seemingly safe internal keys is a critical security anti-pattern as it can lead to arbitrary code execution if inputs ever become unsanitized.
**Prevention:** Always use safe dictionary access methods like `st.session_state.get(key)` instead of dynamically evaluating strings as code.
