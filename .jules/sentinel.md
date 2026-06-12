## 2026-06-12 - Prevent Path Traversal in File Operations
**Vulnerability:** Path traversal in file save and upload operations allowed arbitrary file writes outside intended directories via unsanitized filenames.
**Learning:** User-provided filenames from UI inputs or file uploads must never be trusted directly in file operations, as they can overwrite critical source code.
**Prevention:** Always sanitize user-provided filenames using `os.path.basename()` before using them in file system operations like `os.path.join()` or `open()`.
