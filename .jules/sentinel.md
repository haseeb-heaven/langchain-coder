## 2024-05-24 - Fix eval and Path Traversal Vulnerabilities
**Vulnerability:**
1. `eval()` was used to dynamically evaluate strings containing `st.session_state` keys in `script.py`. This is an arbitrary code execution risk if those strings are ever user-controlled or influenced.
2. `uploadedfile.name` was appended directly to a path using `os.path.join()` in `libs/general_utils.py`. This is a path traversal vulnerability as uploaded file names can contain `../` sequences, allowing arbitrary file writes outside the intended directory.

**Learning:**
1. `eval()` is often mistakenly used as a shortcut for dynamic variable lookups, particularly in dynamically typed environments like Python and Streamlit, instead of using safe dictionary get methods.
2. The `name` property of uploaded files from frameworks like Streamlit should never be trusted. They retain the exact filename provided by the client, including any potentially malicious path components.

**Prevention:**
1. Never use `eval()` for dynamic variable resolution or state checks. Always use safer alternatives like `dict.get(key)` or `st.session_state.get(key)`.
2. Always sanitize user-provided filenames using `os.path.basename()` before using them in file system operations (like `os.path.join` or `open`) to strip out any directory traversal characters.
