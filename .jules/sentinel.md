## 2026-09-29 - Fix Path Traversal in file operations
**Vulnerability:** User-provided filenames were used directly in file system operations in `save_code` and `generate_download_link` without sanitization, leading to a path traversal vulnerability.
**Learning:** Always sanitize user-provided file names before using them in file operations to prevent arbitrary file writes/reads or path traversal vulnerabilities.
**Prevention:** Use `os.path.basename()` on all user-supplied filenames before constructing file paths or using them in file-related APIs.
## 2026-10-12 - Prevent Stack Trace Exposure in Frontend
**Vulnerability:** Unhandled exceptions exposed detailed internal stack traces to the frontend UI via Streamlit `st.toast(traceback.format_exc())`, potentially leaking sensitive paths or logic to malicious users.
**Learning:** Raw stack traces should only be written to secure backend logs, never displayed to the user.
**Prevention:** Replace direct traceback UI rendering with generic, sanitized error messages while maintaining detailed backend logging.
