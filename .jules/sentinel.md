## 2026-09-29 - Fix Path Traversal in file operations
**Vulnerability:** User-provided filenames were used directly in file system operations in `save_code` and `generate_download_link` without sanitization, leading to a path traversal vulnerability.
**Learning:** Always sanitize user-provided file names before using them in file operations to prevent arbitrary file writes/reads or path traversal vulnerabilities.
**Prevention:** Use `os.path.basename()` on all user-supplied filenames before constructing file paths or using them in file-related APIs.

## 2026-10-14 - Prevent Information Leakage in UI
**Vulnerability:** The application exposed full internal Python stack traces directly to the user interface via Streamlit's `st.toast(traceback.format_exc())`. This can reveal sensitive backend file paths, package versions, and system architecture to potential attackers.
**Learning:** Never display raw exception traces or internal errors to end users, as this violates the "Fail Securely" principle and leaks information.
**Prevention:** Always catch exceptions, log the full traceback securely on the backend (e.g., using `logger.error()`), and show only a safe, generic error message to the user on the frontend.
