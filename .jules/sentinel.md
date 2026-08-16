## 2026-08-16 - [Path Traversal in File Upload]
**Vulnerability:** Path traversal risk due to unsanitized `uploadedfile.name` in `os.path.join` within `libs/general_utils.py`.
**Learning:** User-provided file names can contain directory traversal sequences (e.g., `../`) which can allow files to be saved outside the intended directory.
**Prevention:** Always sanitize user-provided filenames using `os.path.basename()` before using them in file system operations.
