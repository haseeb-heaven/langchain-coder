## 2026-06-30 - Fix eval() Security Anti-pattern
**Vulnerability:** Use of `eval()` to dynamically evaluate strings representing `st.session_state` attributes in `script.py`.
**Learning:** Using `eval()` for state checks is a dangerous security anti-pattern that can lead to arbitrary code execution if inputs are influenced by user data.
**Prevention:** Access dictionaries or state objects directly using safe methods like `st.session_state.get(key)` instead of evaluating code strings.
