## 2026-09-29 - Fix Path Traversal in file operations
**Vulnerability:** User-provided filenames were used directly in file system operations in `save_code` and `generate_download_link` without sanitization, leading to a path traversal vulnerability.
**Learning:** Always sanitize user-provided file names before using them in file operations to prevent arbitrary file writes/reads or path traversal vulnerabilities.
**Prevention:** Use `os.path.basename()` on all user-supplied filenames before constructing file paths or using them in file-related APIs.
## 2026-10-09 - Prevent Stack Trace Information Leakage
**Vulnerability:** Raw exception stack traces were directly displayed to the user via UI components (e.g., `st.toast(traceback.format_exc())`), which leaks sensitive internal application details.
**Learning:** Never expose raw internal exceptions directly to end users, as stack traces can reveal sensitive information about the application's underlying architecture, file paths, and environment.
**Prevention:** Catch exceptions and log the full traceback securely on the server-side, but provide only a generic, safe error message to the user frontend.
