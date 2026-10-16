## 2026-09-29 - Fix Path Traversal in file operations
**Vulnerability:** User-provided filenames were used directly in file system operations in `save_code` and `generate_download_link` without sanitization, leading to a path traversal vulnerability.
**Learning:** Always sanitize user-provided file names before using them in file operations to prevent arbitrary file writes/reads or path traversal vulnerabilities.
**Prevention:** Use `os.path.basename()` on all user-supplied filenames before constructing file paths or using them in file-related APIs.
## 2026-10-16 - Prevent stack trace exposure in UI
**Vulnerability:** Application exceptions exposed full stack traces directly to the user interface via `st.toast(traceback.format_exc())`, potentially revealing sensitive system internals or application logic.
**Learning:** Never pass raw exception details or stack traces to UI components. Doing so exposes system information that attackers could leverage to understand the application's architecture or find further vulnerabilities.
**Prevention:** Always catch exceptions, log the full traceback securely on the backend (e.g., using `logger.error(traceback.format_exc())`), and display only a generic, safe error message to the frontend (e.g., `st.toast(f"Error: {str(e)}")`).
