## 2026-08-22 - [Path Traversal in File Upload]
**Vulnerability:** [The `save_uploaded_file_temp` method directly used the user-provided `uploadedfile.name` in `os.path.join` without sanitization, creating a path traversal vulnerability.]
**Learning:** [User-supplied filenames can contain directory traversal characters like `../`, allowing attackers to write files outside the intended temporary directory, potentially overwriting critical system files.]
**Prevention:** [Always sanitize user-provided filenames using functions like `os.path.basename()` before using them in file system operations like `os.path.join` or `open`.]
