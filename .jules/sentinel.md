## 2024-05-15 - Remove eval() for checking session state keys
**Vulnerability:** Arbitrary code execution vulnerability through `eval()`.
**Learning:** Using `eval()` to dynamically check variable truthiness in dictionaries exposes the application to arbitrary code execution if the key strings can be manipulated.
**Prevention:** Never use `eval()` to dynamically evaluate code strings or check dictionary values. Instead, use safer alternatives like `st.session_state.get(key)` or explicit boolean checks on the variables directly.
