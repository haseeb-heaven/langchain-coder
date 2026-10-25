## 2026-09-29 - Fix Path Traversal in file operations
**Vulnerability:** User-provided filenames were used directly in file system operations in `save_code` and `generate_download_link` without sanitization, leading to a path traversal vulnerability.
**Learning:** Always sanitize user-provided file names before using them in file operations to prevent arbitrary file writes/reads or path traversal vulnerabilities.
**Prevention:** Use `os.path.basename()` on all user-supplied filenames before constructing file paths or using them in file-related APIs.

## 2024-05-24 - Cross-Site Scripting (XSS) Vulnerability in HTML Generation
**Vulnerability:** The application dynamically generates HTML templates (for JDoodle Compiler iFrame embedding) by inserting user-supplied content (`code_prompt`) via string formatting `.format(language=..., script_code=code_prompt)`. The `code_prompt` is not escaped, meaning if a user provides a prompt containing HTML tags or JavaScript code (e.g., `<script>alert(1)</script>`), it will be injected and executed directly in the generated output, leading to an XSS vulnerability.
**Learning:** Whenever injecting user-controlled data into HTML templates, it is critical to properly escape the content to prevent it from being interpreted as executable code (HTML or JavaScript) by the browser. Python's built-in `html` module provides the necessary `html.escape()` function.
**Prevention:** Always use `html.escape()` when inserting user input into dynamic HTML generation to sanitize the input and mitigate XSS risks.
