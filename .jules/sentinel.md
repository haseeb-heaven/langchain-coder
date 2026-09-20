## 2026-09-20 - [Path Traversal in Uploaded File Temp Saving]
**Vulnerability:** Path traversal vulnerability due to unsanitized `uploadedfile.name` being used directly in `os.path.join(temp_dir, uploadedfile.name)`.
**Learning:** Always sanitize user-provided filenames, such as those from file uploads, before using them in file system operations. An attacker could potentially write files outside the intended directory.
**Prevention:** Use `os.path.basename()` to extract only the filename part of the path, ensuring the file is saved exactly where intended.
