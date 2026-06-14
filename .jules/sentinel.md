
## 2026-06-14 - Remove Dangerous eval() Usage
**Vulnerability:** Arbitrary code execution risk via the use of `eval()` to check dictionary keys mapped to session state variables.
**Learning:** Using `eval()` even for internal configuration checking is an anti-pattern that can lead to severe security flaws if user input or unexpected variables ever reach that path.
**Prevention:** Use safer dictionary access methods like `st.session_state.get(key)` instead of dynamically evaluating strings as code.
