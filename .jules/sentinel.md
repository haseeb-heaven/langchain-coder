## 2026-09-29 - Fix Path Traversal in file operations
**Vulnerability:** User-provided filenames were used directly in file system operations in `save_code` and `generate_download_link` without sanitization, leading to a path traversal vulnerability.
**Learning:** Always sanitize user-provided file names before using them in file operations to prevent arbitrary file writes/reads or path traversal vulnerabilities.
**Prevention:** Use `os.path.basename()` on all user-supplied filenames before constructing file paths or using them in file-related APIs.
## 2026-10-08 - Stack Trace Information Leakage

**Vulnerability:** The application was displaying raw stack traces directly to the user interface via `st.toast()`.
**Learning:** Displaying internal exceptions (like `traceback.format_exc()`) to users via the frontend reveals internal system details, presenting a security risk. All errors should be safely logged on the backend.
**Prevention:** Avoid passing raw exception messages or stack traces to `st.toast()`. Always use generic error messages for the UI and log the detailed stack trace to the backend using the logging module.
