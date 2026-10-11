## 2026-09-29 - Fix Path Traversal in file operations
**Vulnerability:** User-provided filenames were used directly in file system operations in `save_code` and `generate_download_link` without sanitization, leading to a path traversal vulnerability.
**Learning:** Always sanitize user-provided file names before using them in file operations to prevent arbitrary file writes/reads or path traversal vulnerabilities.
**Prevention:** Use `os.path.basename()` on all user-supplied filenames before constructing file paths or using them in file-related APIs.
## 2026-10-11 - Prevent Stack Trace Leakage in Frontend
**Vulnerability:** The application was exposing full Python stack traces to the user via `st.toast()` during error handling in `libs/general_utils.py`.
**Learning:** Directly rendering `traceback.format_exc()` on the frontend allows potential attackers to understand internal structures, file paths, and dependencies, which facilitates targeted attacks.
**Prevention:** Always log the full `traceback.format_exc()` securely on the backend using standard logging (e.g., `logger.error()`) and return a safe, generic error message or the sanitized exception string to the user.
