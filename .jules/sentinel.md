
## 2026-06-11 - Fix eval and path traversal vulnerabilities
**Vulnerability:**
1. The `save_uploaded_file` function in `libs/general_utils.py` concatenated `temp_dir` with the unsanitized `uploadedfile.name`, making it vulnerable to path traversal.
2. The UI error handling logic in `script.py` used `eval()` to check values inside `st.session_state`, leading to arbitrary code execution risks.

**Learning:**
1. Direct use of user-controlled properties (like file names) in path constructors (`os.path.join`) without sanitization easily creates path traversal vulnerabilities.
2. Using `eval()` on strings that contain references to application state is extremely risky and unnecessary when safe lookup methods (like `.get()`) exist.

**Prevention:**
1. Always sanitize user-provided filenames using `os.path.basename()` before combining them with directories.
2. Avoid `eval()` completely. Use dictionary key lookups (e.g., `dict.get(key)`) for safe dynamic value retrieval.
