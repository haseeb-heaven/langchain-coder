## 2026-09-29 - Fix Path Traversal in file operations
**Vulnerability:** User-provided filenames were used directly in file system operations in `save_code` and `generate_download_link` without sanitization, leading to a path traversal vulnerability.
**Learning:** Always sanitize user-provided file names before using them in file operations to prevent arbitrary file writes/reads or path traversal vulnerabilities.
**Prevention:** Use `os.path.basename()` on all user-supplied filenames before constructing file paths or using them in file-related APIs.
## 2026-10-10 - Stack Trace Leakage via UI
**Vulnerability:** Exposed raw exception stack traces (`traceback.format_exc()`) to users via Streamlit's `st.toast()`.
**Learning:** Returning detailed internal errors (like file paths, library versions, or structure) directly to the frontend exposes internal application mechanics to potential attackers.
**Prevention:** Always catch exceptions, log the full `traceback.format_exc()` on the backend using `logger.error()`, and return a generic or safe error message to the user.
