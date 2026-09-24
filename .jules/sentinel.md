
## 2026-09-24 - Path Traversal Vulnerability in File Operations
**Vulnerability:** User-provided filenames in file upload (`save_uploaded_file_temp`) and code saving (`save_code`) functions were used directly in `os.path.join` and `open()` without sanitization, allowing path traversal (e.g., using `../` to write outside intended directories).
**Learning:** Even when files are saved to seemingly constrained directories (like temporary folders or extension-specific folders), unsanitized user filenames can break out of these constraints if they contain directory traversal sequences.
**Prevention:** Always sanitize user-provided filenames using `os.path.basename()` to strip any directory paths before using them in file system operations.
