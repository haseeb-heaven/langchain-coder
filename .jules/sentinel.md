## 2026-07-11 - Path Traversal Vulnerability
**Vulnerability:** Path traversal vulnerability due to unsanitized file names.
**Learning:** User-provided file names were used directly in file system operations without sanitization.
**Prevention:** Always sanitize user-provided file names using `os.path.basename` before using them in file system operations.
