## 2026-07-06 - Prevent Path Traversal in File Saves
**Vulnerability:** The `save_code` function used unsanitized user-provided filenames to write files, allowing path traversal (e.g., `../../../file.py`) which could overwrite arbitrary files.
**Learning:** Even internal tool functionalities that write to local disk must sanitize input filenames, as they can be exploited to overwrite sensitive application files.
**Prevention:** Always use `os.path.basename()` on user-provided filenames before using them in file system operations like `open` or `os.path.join`.

## 2026-07-06 - Remove Insecure eval() Usage
**Vulnerability:** The codebase used `eval()` to dynamically evaluate variable names from a dictionary to check if Streamlit session state keys were set.
**Learning:** Using `eval()` to check dictionary or state values is a security anti-pattern that can lead to arbitrary code execution if the input ever becomes user-controlled.
**Prevention:** Avoid `eval()`. Use safer alternatives like `st.session_state.get(key)` to retrieve and check values securely.
