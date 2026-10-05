## 2026-09-29 - Fix Path Traversal in file operations
**Vulnerability:** User-provided filenames were used directly in file system operations in `save_code` and `generate_download_link` without sanitization, leading to a path traversal vulnerability.
**Learning:** Always sanitize user-provided file names before using them in file operations to prevent arbitrary file writes/reads or path traversal vulnerabilities.
**Prevention:** Use `os.path.basename()` on all user-supplied filenames before constructing file paths or using them in file-related APIs.
## 2026-10-05 - Prevent Information Leakage in UI
**Vulnerability:** Stack traces and sensitive internal error details were leaked to the user interface via `st.toast(traceback.format_exc())`.
**Learning:** Exposing detailed exceptions to the UI (even if helpful for debugging) can give attackers insight into the internal structure of the application.
**Prevention:** Catch blocks should log the detailed stack trace on the backend using `logger.error` while displaying a safe, generic error message to the frontend.
