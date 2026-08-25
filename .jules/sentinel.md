## 2026-08-25 - [Path Traversal in Uploaded Files]
**Vulnerability:** User-provided filename in `save_uploaded_file_temp` was directly joined with the temporary directory path, allowing for path traversal vulnerabilities.
**Learning:** Malicious actors could craft a POST request with a full path like `../../../etc/passwd` to write files outside the intended directory.
**Prevention:** Always sanitize user-provided filenames using `os.path.basename()` before using them in file system operations.
