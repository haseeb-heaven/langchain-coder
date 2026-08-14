## 2026-08-14 - Arbitrary Code Execution via eval()

**Vulnerability:** The application uses `eval()` to evaluate variable names dynamically constructed as strings when checking unset configuration items in `script.py`.
**Learning:** Using `eval()` to evaluate strings is extremely dangerous and can lead to arbitrary code execution, especially if any part of the evaluated string ever becomes user-controllable.
**Prevention:** Avoid `eval()` completely. Instead of building strings like 'st.session_state.project' and evaluating them, check the state keys directly using safe dictionary access methods, such as `st.session_state.get('project')`.
