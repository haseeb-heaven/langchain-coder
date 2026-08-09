## 2026-08-09 - Critical Security Fixes
**Vulnerability:** Arbitrary code execution via `eval()` for Streamlit session state and Path Traversal vulnerability when saving uploaded files.
**Learning:** Using `eval()` to dynamically read state variables is a severe security risk. Filenames from uploaded files should never be trusted and used directly in file paths.
**Prevention:** Always use safe access methods like `st.session_state.get(key)`. Always sanitize filenames using `os.path.basename()` before saving.
