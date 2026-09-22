## 2026-09-22 - Prevent Path Traversal in File Saves
**Vulnerability:** User input for file names during code saving was not sanitized, allowing path traversal (e.g., ../../../).
**Learning:** Always sanitize user-provided file names before using them in file system operations like opening or saving.
**Prevention:** Use os.path.basename() on filename inputs to strip any path components before processing or using them in os.path.join.
