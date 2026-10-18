## 2026-09-29 - Fix Path Traversal in file operations
**Vulnerability:** User-provided filenames were used directly in file system operations in `save_code` and `generate_download_link` without sanitization, leading to a path traversal vulnerability.
**Learning:** Always sanitize user-provided file names before using them in file operations to prevent arbitrary file writes/reads or path traversal vulnerabilities.
**Prevention:** Use `os.path.basename()` on all user-supplied filenames before constructing file paths or using them in file-related APIs.

## 2026-10-18 - Prevent Information Leakage via Frontend Error Messages
**Vulnerability:** The application was exposing full internal Python stack traces directly to the user interface via `st.toast(traceback.format_exc())` when exceptions occurred during file saving or download link generation.
**Learning:** While full stack traces are essential for debugging and should be logged on the backend, displaying them to the frontend user leaks internal application structure, file paths, and potentially sensitive environment or dependency information.
**Prevention:** Always log detailed exception traces securely on the backend (e.g., using `logger.error(traceback.format_exc())`) and display only safe, generic, and user-friendly error messages on the frontend (e.g., `st.toast(f"Error: {e}", icon="❌")`). Avoid directly exposing `traceback.format_exc()` or raw error details to the user interface.
