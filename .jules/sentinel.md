## 2026-09-26 - Path Traversal via Unsanitized Filenames
**Vulnerability:** User-provided filenames in `save_code` and `save_uploaded_file_temp` were directly concatenated into file paths without sanitization, leading to arbitrary file write / path traversal vulnerabilities.
**Learning:** Streamlit apps often handle file uploads or file naming inputs dynamically. Without proper sanitization, this input exposes the underlying server file system.
**Prevention:** Always use `os.path.basename()` on user-provided file names or upload objects (`uploadedfile.name`) before executing any I/O operations like `open()` or `os.path.join()`.
