## 2026-09-28 - Path Traversal Vulnerability
**Vulnerability:** Found path traversal vulnerability when saving code or temp files using user-provided inputs (`file_name` and `uploadedfile.name`) in `libs/general_utils.py`.
**Learning:** File names should always be sanitized using `os.path.basename()` before writing to disk to avoid writing files in arbitrary directories.
**Prevention:** Always wrap user-provided file names or paths from upload objects with `os.path.basename()` before using them in filesystem operations.
