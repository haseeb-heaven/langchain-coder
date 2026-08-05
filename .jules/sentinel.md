## 2026-08-05 - [Remove Unsafe eval() in Vertex AI Validation]
**Vulnerability:** The application used Python's eval() to dynamically check st.session_state variable existence in script.py. While the current inputs were hardcoded strings representing state keys, eval() is an unsafe, critical vulnerability anti-pattern that can lead to arbitrary code execution if user input ever reaches it.
**Learning:** Checking state values should be done securely using dictionary lookup methods (like dict.get() or direct access) rather than dynamically evaluating string literals as code.
**Prevention:** Never use eval() for dictionary or state object access. Always use safer alternatives like st.session_state.get(key).
