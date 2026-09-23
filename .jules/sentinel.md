## 2026-09-23 - Prevent Path Traversal in File Operations
**Vulnerability:** The application was using unsanitized user inputs (`file_name` in `save_code` and `uploadedfile.name` in `save_uploaded_file_temp`) in file system paths. This could allow an attacker to write files outside of the intended directory using path traversal characters like `../`.
**Learning:** Always sanitize filenames provided by users or external sources before using them in file operations (`os.path.join` or `open`).
**Prevention:** Use `os.path.basename()` on user-provided filenames to strip any path components and ensure only the base filename is used.
