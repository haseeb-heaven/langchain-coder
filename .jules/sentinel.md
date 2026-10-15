## 2026-09-29 - Fix Path Traversal in file operations
**Vulnerability:** User-provided filenames were used directly in file system operations in `save_code` and `generate_download_link` without sanitization, leading to a path traversal vulnerability.
**Learning:** Always sanitize user-provided file names before using them in file operations to prevent arbitrary file writes/reads or path traversal vulnerabilities.
**Prevention:** Use `os.path.basename()` on all user-supplied filenames before constructing file paths or using them in file-related APIs.
## 2026-10-15 - Prevent stack trace leakage in Streamlit toast
**Vulnerability:** Frontend exceptions were dumping the full `traceback.format_exc()` into `st.toast()`, potentially leaking sensitive internal implementation details or server paths to the user.
**Learning:** Using Streamlit UI components (like `st.toast`) to display raw exception traces creates information leakage. Stack traces should strictly remain in backend server logs.
**Prevention:** Always log the full traceback securely on the backend (e.g., using `logger.error()`) and provide only a safe, generic error message (e.g., `st.toast(f"Error: {e}")`) to the frontend.
