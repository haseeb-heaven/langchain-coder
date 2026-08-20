## 2026-08-20 - Remove eval() to prevent arbitrary code execution

**Vulnerability:** The use of `eval(var)` to dynamically check Streamlit session state properties. If `var` can be manipulated or improperly sanitized, it could lead to arbitrary Python code execution.
**Learning:** Using `eval()` even for seemingly benign checks is a bad practice and poses an unnecessary security risk.
**Prevention:** Avoid `eval()` entirely for dynamic attribute access. Rely on safer methods like dictionary lookups, e.g., `st.session_state.get(key)`.
