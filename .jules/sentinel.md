## 2026-09-30 - Fix Path Traversal Vulnerabilities

**Vulnerability:** User-provided file names were concatenated to directory paths without sanitization in file-saving functions (save_code, generate_download_link, save_uploaded_file_temp), potentially allowing path traversal attacks.

**Learning:** When dealing with files and dynamic names from requests or user input, never trust the filename blindly; an attacker could provide names like '../../../etc/passwd' to write files to arbitrary locations.

**Prevention:** Always sanitize the filename by applying os.path.basename() before using it in file path operations.
