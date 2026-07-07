## 2026-07-07 - Fix eval() Vulnerability in State Checks
**Vulnerability:** Arbitrary code execution via the use of `eval()` to dynamically evaluate strings representing `st.session_state` keys in `script.py`.
**Learning:** Using `eval()` is a critical security risk and a known anti-pattern. While the inputs in this specific instance were hardcoded dictionary keys, using `eval()` sets a dangerous precedent and can easily lead to arbitrary code execution if user inputs or external data are ever introduced into the evaluation flow.
**Prevention:** Never use `eval()` for dynamic string evaluation. Instead, directly access state values using safer alternatives like `st.session_state.get(key)`.
