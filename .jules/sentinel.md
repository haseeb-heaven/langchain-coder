## 2024-05-18 - Path Traversal in File Saving and Upload
**Vulnerability:** The application was vulnerable to path traversal (CRITICAL) in `libs/general_utils.py` where `file_name` in `save_code` and `uploadedfile.name` in `save_uploaded_file_temp` were used directly in file system operations without sanitization.
**Learning:** Even internal utility functions that handle files or uploads must treat user-provided filenames as untrusted data.
**Prevention:** Always sanitize filenames using `os.path.basename()` before constructing file paths or performing file system operations.

## 2024-05-18 - Dangerous eval() Usage for Variable Checking
**Vulnerability:** The application used `eval()` to dynamically check the presence of variables in the `st.session_state` dictionary (HIGH). While the strings were currently hardcoded, `eval()` is a security anti-pattern that can lead to arbitrary code execution if strings become user-controlled. It also causes performance overhead and potential exceptions.
**Learning:** `eval()` should never be used to check dictionary values or dynamically evaluate code strings if safer alternatives exist.
**Prevention:** Use standard dictionary methods like `dict.get(key)` to safely check for the presence and truthiness of values in state objects like `st.session_state`.
