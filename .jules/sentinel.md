## 2024-05-24 - Remove eval() to prevent Arbitrary Code Execution

**Vulnerability:** Found `eval(var)` being used to evaluate state variables (`st.session_state.project` etc). This is extremely dangerous as it can lead to arbitrary code execution if user inputs find their way into these variables.
**Learning:** Checking states or retrieving dynamic dictionary values should never use `eval()`.
**Prevention:** Use `st.session_state.get(var)` or similar safe dictionary accesses instead of `eval(var)`.
