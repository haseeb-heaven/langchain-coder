## 2026-09-29 - Fix Path Traversal in file operations
**Vulnerability:** User-provided filenames were used directly in file system operations in `save_code` and `generate_download_link` without sanitization, leading to a path traversal vulnerability.
**Learning:** Always sanitize user-provided file names before using them in file operations to prevent arbitrary file writes/reads or path traversal vulnerabilities.
**Prevention:** Use `os.path.basename()` on all user-supplied filenames before constructing file paths or using them in file-related APIs.
## 2026-10-23 - Prevent Information Leakage in UI Notifications
**Vulnerability:** The application was exposing full stack traces to the frontend UI via `st.toast(traceback.format_exc())`, potentially leaking sensitive internal directory structures and implementation details to end users.
**Learning:** Error handling mechanisms must be bifurcated: detailed logs for the backend (using `logger.error(traceback.format_exc())`) and sanitized, generic messages for the frontend (using `st.toast(str(e))`).
**Prevention:** Never pass raw exception objects or tracebacks to UI components. Always catch exceptions, log the full trace securely on the server side, and return a safe, abstract error message to the user.
