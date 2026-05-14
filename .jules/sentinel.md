## 2024-05-23 - Dynamic Evaluation of Session State
**Vulnerability:** Arbitrary code execution via `eval()` used to dynamically evaluate dictionary keys corresponding to session state variables (`eval("st.session_state.project")`).
**Learning:** Developers used `eval()` as a shortcut to check if dynamically generated variable names were set in Streamlit's session state. This is a severe anti-pattern in Streamlit apps that could allow arbitrary code execution if the variable string ever incorporates user input.
**Prevention:** Always use safe dictionary access methods like `st.session_state.get(key)` instead of dynamically evaluating strings as Python code.

## 2024-05-23 - Path Traversal in File Uploads
**Vulnerability:** Unsanitized user-provided filename used in `os.path.join` allowing potential path traversal.
**Learning:** `uploadedfile.name` should never be trusted as it can contain characters like `../` to navigate outside the intended directory.
**Prevention:** Always use `os.path.basename()` to sanitize filenames before file system operations.
