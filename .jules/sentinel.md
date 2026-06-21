## 2026-06-21 - Path Traversal in File Saving and Uploads
**Vulnerability:** User-provided file names in `save_code` and `save_uploaded_file_temp` were directly used in file operations, allowing path traversal (e.g., saving files outside the intended directory).
**Learning:** We must never trust user-supplied filenames directly in filesystem operations, even for temporary files or within specific workflows.
**Prevention:** Always use `os.path.basename()` to extract just the filename component from user input before joining paths or opening files.
