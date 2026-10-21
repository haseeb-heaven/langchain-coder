## 2026-09-29 - Fix Path Traversal in file operations
**Vulnerability:** User-provided filenames were used directly in file system operations in `save_code` and `generate_download_link` without sanitization, leading to a path traversal vulnerability.
**Learning:** Always sanitize user-provided file names before using them in file operations to prevent arbitrary file writes/reads or path traversal vulnerabilities.
**Prevention:** Use `os.path.basename()` on all user-supplied filenames before constructing file paths or using them in file-related APIs.
## 2026-10-21 - Prevent Stack Trace Leakage to Frontend
**Vulnerability:** The application was exposing full internal stack traces to the user interface via `st.toast(traceback.format_exc())` when exceptions occurred during file operations, revealing sensitive system and code details.
**Learning:** Using generic try/except blocks that output the full traceback to the UI is a risky pattern that leaks internal application state. Frontend error messages must always be sanitized.
**Prevention:** Always log the full traceback securely on the backend using `logger.error` while displaying only a safe, generic error message (like `str(e)`) to the user via UI components.
