## 2026-10-03 - Path Traversal Vulnerability Fix
**Vulnerability:** User-provided filenames in `save_code` and `save_uploaded_file_temp` in `libs/general_utils.py` were not sanitized, allowing for path traversal attacks if malicious filenames (like `../../../etc/passwd`) were provided.
**Learning:** Always sanitize user-provided file inputs before using them in file system operations like `open()` or `os.path.join()`.
**Prevention:** To prevent directory traversal while still supporting subdirectories, resolve the final absolute path using `os.path.abspath(os.path.join(base_dir, file_name))` and verify that it strictly starts with the intended base workspace directory (e.g., `file_path.startswith(base_dir + os.sep)`).
