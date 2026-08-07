## 2026-08-07 - Path Traversal in File Upload
**Vulnerability:** Unsanitized user-provided filename used in file system operations.
**Learning:** Always sanitize user-provided filenames using `os.path.basename()` before using them in file system operations (like `os.path.join` or `open`) to prevent path traversal vulnerabilities.
**Prevention:** Sanitize user input and follow the principle of least privilege.
