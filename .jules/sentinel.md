## 2026-09-29 - Fix Path Traversal in file operations
**Vulnerability:** User-provided filenames were used directly in file system operations in `save_code` and `generate_download_link` without sanitization, leading to a path traversal vulnerability.
**Learning:** Always sanitize user-provided file names before using them in file operations to prevent arbitrary file writes/reads or path traversal vulnerabilities.
**Prevention:** Use `os.path.basename()` on all user-supplied filenames before constructing file paths or using them in file-related APIs.
## 2026-10-26 - Prevent stack trace leaks in UI
**Vulnerability:** Leaking internal stack traces directly to the UI using `traceback.format_exc()` in Streamlit `st.toast()`.
**Learning:** Using `traceback.format_exc()` for user-facing errors exposes internal system details, making it a security risk (Information Exposure).
**Prevention:** Always log the full traceback securely on the backend (e.g., using `logger.error()`) and provide only a safe, generic error message to the frontend.
