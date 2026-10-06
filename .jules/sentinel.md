## 2026-09-29 - Fix Path Traversal in file operations
**Vulnerability:** User-provided filenames were used directly in file system operations in `save_code` and `generate_download_link` without sanitization, leading to a path traversal vulnerability.
**Learning:** Always sanitize user-provided file names before using them in file operations to prevent arbitrary file writes/reads or path traversal vulnerabilities.
**Prevention:** Use `os.path.basename()` on all user-supplied filenames before constructing file paths or using them in file-related APIs.

## 2026-10-06 - Prevent stack trace leakage to UI
**Vulnerability:** The application was exposing full python stack traces directly to the user interface via `st.toast(traceback.format_exc())` on exceptions.
**Learning:** Raw stack traces should not be exposed to the end user as they can leak sensitive information about the internal workings of the application.
**Prevention:** Catch exceptions and present generic, safe error messages to the user interface while logging the full stack trace to the backend logger for debugging purposes.
