## 2026-08-18 - Fix Path Traversal Vulnerability
**Vulnerability:** Path traversal vulnerability discovered in `save_code` method in `libs/general_utils.py`.
**Learning:** The application writes files to the filesystem using user-provided filenames without sanitization, allowing an attacker to potentially write to arbitrary directories by using relative paths like `../../`.
**Prevention:** Always sanitize user-provided filenames using `os.path.basename()` before using them in filesystem operations like `open()` or `os.path.join()`.
