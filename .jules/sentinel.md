## 2026-09-29 - Fix Path Traversal in file operations
**Vulnerability:** User-provided filenames were used directly in file system operations in `save_code` and `generate_download_link` without sanitization, leading to a path traversal vulnerability.
**Learning:** Always sanitize user-provided file names before using them in file operations to prevent arbitrary file writes/reads or path traversal vulnerabilities.
**Prevention:** Use `os.path.basename()` on all user-supplied filenames before constructing file paths or using them in file-related APIs.
## 2026-10-19 - Leaking stack trace to frontend components (st.toast) in Streamlit
**Vulnerability:** Information leakage. Exposing raw stack trace to frontend users.
**Learning:** When using Streamlit, calling `st.toast(traceback.format_exc())` outputs the backend stack trace directly to the frontend.
**Prevention:** Only log `traceback.format_exc()` on the server backend (e.g. `logger.error()`) and use a safe generic error message (e.g. `str(e)` or a generic string) for frontend display via `st.toast()`.
