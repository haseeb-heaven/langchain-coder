## 2024-05-18 - Path Traversal in File Saving and Upload
**Vulnerability:** The application was vulnerable to path traversal (CRITICAL) in `libs/general_utils.py` where `file_name` in `save_code` and `uploadedfile.name` in `save_uploaded_file_temp` were used directly in file system operations without sanitization.
**Learning:** Even internal utility functions that handle files or uploads must treat user-provided filenames as untrusted data.
**Prevention:** Always sanitize filenames using `os.path.basename()` before constructing file paths or performing file system operations.
