## 2024-05-24 - [Title]
**Vulnerability:**
**Learning:**
**Prevention:**
## 2024-05-24 - Arbitrary Code Execution and Path Traversal
**Vulnerability:** Found an eval() used on dynamic strings in script.py and an unsanitized path filename used for file operations in libs/general_utils.py.
**Learning:** eval() can execute arbitrary code on the host, while unsanitized file paths allow path traversal.
**Prevention:** Use safer dictionary accessors like st.session_state.get(var) and sanitize files with os.path.basename(file_name).
