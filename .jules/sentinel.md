## 2026-07-04 - Fix Eval Anti-Pattern and Path Traversal
**Vulnerability:** Arbitrary code execution via `eval()` in `script.py` and path traversal via unsanitized `uploadedfile.name` in `libs/general_utils.py`.
**Learning:** `eval()` should never be used to dynamically check dictionary values or states, and user-provided filenames must always be sanitized before being used in file system operations.
**Prevention:** Use safer alternatives like `dict.get(key)` or `st.session_state.get(key)` instead of `eval()`. Always sanitize filenames using `os.path.basename()` before using them in file operations.
