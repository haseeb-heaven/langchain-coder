## 2026-06-24 - Prevent Plaintext Credential Logging and Path Traversal
**Vulnerability:** API key was logged in plaintext via logger.warn(), and user-provided uploadedfile.name was used directly in os.path.join() without sanitization.
**Learning:** Always treat user input, including filenames, as untrusted. Never log sensitive credentials.
**Prevention:** Use os.path.basename() to sanitize filenames before file system operations. Do not log sensitive data like API keys.
