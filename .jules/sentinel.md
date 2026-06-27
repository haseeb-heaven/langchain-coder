## 2026-06-27 - Prevent Path Traversal in Code Saving
**Vulnerability:** The `save_code` method in `libs/general_utils.py` blindly trusted the user-provided `file_name` and used string concatenation to create a file path (`f"{file_extension}/{file_name}"`). This allowed path traversal (e.g., passing `../../../etc/passwd`).
**Learning:** Always sanitize user-provided filenames before using them in file system operations.
**Prevention:** Use `os.path.basename()` to extract only the final filename component and `os.path.join()` to construct safe paths, preventing directory traversal attacks.
