## 2026-07-17 - Fix Eval and Path Traversal Vulnerabilities
**Vulnerability:** Arbitrary Code Execution via eval() on session state variable names in `script.py` and Path Traversal via unsanitized uploaded filename in `libs/general_utils.py`.
**Learning:** Using eval() to dynamically evaluate code strings is dangerous and should be avoided in favor of dictionary lookups. Uploaded filenames must be sanitized to prevent files from being written outside intended directories.
**Prevention:** Use `st.session_state.get(key)` instead of eval() and `os.path.basename(filename)` to sanitize filenames.
