## 2026-07-11 - Path Traversal Vulnerability
**Vulnerability:** Path traversal vulnerability due to unsanitized file names.
**Learning:** User-provided file names were used directly in file system operations without sanitization.
**Prevention:** Always sanitize user-provided file names using `os.path.basename` before using them in file system operations.
## 2026-10-17 - Prevent stack trace leakage in Streamlit UI
**Vulnerability:** The application was exposing full stack traces to the user interface via `st.toast(traceback.format_exc())` in `libs/general_utils.py`, which is a security risk as it can reveal sensitive internal architecture, file paths, and environment details.
**Learning:** In Streamlit applications, exception handling should never display internal stack traces directly to the user.
**Prevention:** Always log the full traceback securely on the backend (e.g., using `logger.error()`) and provide only a safe, generic error message to the frontend (e.g., `st.toast("An error occurred. Please check the logs.", icon="❌")`).
