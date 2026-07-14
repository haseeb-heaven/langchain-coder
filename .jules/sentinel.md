## 2026-07-14 - Remove eval() anti-pattern in session state checks
**Vulnerability:** Arbitrary code execution vulnerability through eval() used to check dictionary string values.
**Learning:** Using eval() to dynamically evaluate code strings for state checks is a dangerous security anti-pattern that can lead to arbitrary code execution if input is not fully trusted or can be modified.
**Prevention:** Never use eval() for checking dictionary or state values. Instead, use safer alternatives like dict.get(key) or st.session_state.get(key).
