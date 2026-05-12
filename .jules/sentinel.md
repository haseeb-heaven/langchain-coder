## 2024-05-18 - [Path Traversal in Uploaded Files & Insecure eval()]
**Vulnerability:** Found two critical security issues:
1. Path traversal via unsanitized `uploadedfile.name` used directly in `os.path.join(temp_dir, uploadedfile.name)` in `libs/general_utils.py`.
2. Arbitrary code execution via `eval(var)` in `script.py` used to dynamically check dictionary values for `st.session_state`.

**Learning:**
1. Filenames from untrusted sources (like user uploads) should never be trusted or concatenated directly into paths.
2. The `eval()` function is highly dangerous and shouldn't be used for accessing dynamic variables, especially when safe alternatives like dictionary `get()` or simple attribute access exist.

**Prevention:**
1. Always sanitize filenames using `os.path.basename(filename)` before using them in file system operations.
2. Never use `eval()` to check dictionary keys or session state variables; use safe alternatives like `dict.get(key)`.
