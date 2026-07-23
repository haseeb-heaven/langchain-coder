## 2026-07-23 - [Path Traversal in Upload Handler]
**Vulnerability:** User-provided filename was used directly in `os.path.join(temp_dir, uploadedfile.name)` without sanitization, allowing path traversal (e.g., `../../`) outside the intended directory.
**Learning:** Filenames from untrusted sources (like uploaded files) must never be trusted. They can contain directory traversal sequences that trick the server into writing files to unintended locations, potentially leading to arbitrary code execution or overwriting critical system files.
**Prevention:** Always sanitize user-provided filenames using `os.path.basename(filename)` before using them in file system operations to ensure the file is saved exactly in the intended directory.
