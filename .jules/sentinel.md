## 2026-09-29 - Fix Path Traversal in file operations
**Vulnerability:** User-provided filenames were used directly in file system operations in `save_code` and `generate_download_link` without sanitization, leading to a path traversal vulnerability.
**Learning:** Always sanitize user-provided file names before using them in file operations to prevent arbitrary file writes/reads or path traversal vulnerabilities.
**Prevention:** Use `os.path.basename()` on all user-supplied filenames before constructing file paths or using them in file-related APIs.

## 2026-10-22 - Prevent Information Leakage in UI
**Vulnerability:** Detailed stack traces were exposed directly to the user interface via `st.toast`, which can reveal sensitive system or application architecture details.
**Learning:** Never expose raw stack traces (`traceback.format_exc()`) to frontend elements in Streamlit applications. This is a form of information leakage.
**Prevention:** Always log the full traceback securely on the backend (e.g., using `logger.error()`) and provide only a safe, generic error message to the frontend (e.g., using `str(e)`).
