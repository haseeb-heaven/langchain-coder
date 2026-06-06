## 2026-06-06 - Remove eval() usage in validation logic
**Vulnerability:** Arbitrary code execution vulnerability through the use of `eval()` to check session state variable values in the Vertex AI settings validation logic.
**Learning:** Using `eval()` to parse dictionary keys as Python code strings is a dangerous anti-pattern that can lead to remote code execution if the variables being evaluated contain unsanitized user input.
**Prevention:** Use safe dictionary access methods like `st.session_state.get(key)` to fetch values securely instead of dynamically evaluating strings as code.
