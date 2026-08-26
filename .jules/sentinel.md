## 2026-08-26 - Arbitrary Code Execution via eval()
**Vulnerability:** The codebase used `eval()` to evaluate strings representing variables (like `'st.session_state.project'`) to check their presence, creating an arbitrary code execution risk if input is ever injected.
**Learning:** Using `eval()` for dynamic state or dictionary lookups is a dangerous anti-pattern. While this specific instance used hardcoded strings, it normalizes a highly dangerous function that could be extrapolated to user input.
**Prevention:** Always use safe dictionary lookups (e.g., `st.session_state.get(key)`) instead of parsing strings dynamically with `eval()`.
