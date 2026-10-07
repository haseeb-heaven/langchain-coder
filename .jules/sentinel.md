## 2026-09-29 - Fix Path Traversal in file operations
**Vulnerability:** User-provided filenames were used directly in file system operations in `save_code` and `generate_download_link` without sanitization, leading to a path traversal vulnerability.
**Learning:** Always sanitize user-provided file names before using them in file operations to prevent arbitrary file writes/reads or path traversal vulnerabilities.
**Prevention:** Use `os.path.basename()` on all user-supplied filenames before constructing file paths or using them in file-related APIs.

## 2026-10-07 - Prevent Information Disclosure via UI Stack Traces
**Vulnerability:** The application was exposing full Python stack traces directly to the user interface via `st.toast(traceback.format_exc())` when exceptions occurred during file save or download operations.
**Learning:** Displaying internal stack traces to end-users is a medium-severity security risk as it can leak sensitive information about the backend architecture, file paths, and application logic.
**Prevention:** Always log the full `traceback.format_exc()` securely on the backend (e.g., using `logger.error()`) and provide only a safe, generic error message (e.g., `str(e)`) to the frontend using `st.toast()`.
