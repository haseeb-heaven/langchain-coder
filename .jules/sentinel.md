## 2026-09-27 - Path Traversal Vulnerability in File Uploads and Saving
**Vulnerability:** User-provided filenames (`uploadedfile.name` and `file_name`) were used directly in `os.path.join()` and string formatting to create file paths without sanitization, leading to arbitrary file write vulnerabilities (Path Traversal).
**Learning:** Filenames coming from user input or external sources (like Streamlit `UploadedFile`) must always be treated as untrusted. They can contain directory traversal sequences (e.g., `../../`).
**Prevention:** Always sanitize user-provided filenames using `os.path.basename()` before using them in file system operations (like `os.path.join` or `open`).
