## 2026-09-18 - Path Traversal in File Saving
**Vulnerability:** Path traversal via unsanitized user-supplied filename in `save_code`.
**Learning:** `file_name` was directly used in file paths (e.g., `f"{file_extension}/{file_name}"`), allowing an attacker to write files anywhere.
**Prevention:** Always sanitize filenames from user input using `os.path.basename(filename)` before using them in file system operations.
