## 2026-07-26 - Prevent Path Traversal in File Savings
**Vulnerability:** The application was directly using user-provided filenames in file system operations.
**Learning:** This can lead to a Path Traversal vulnerability where an attacker can write files outside the intended directory.
**Prevention:** Always sanitize user-provided filenames using os.path.basename() before performing file system operations.
