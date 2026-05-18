## 2024-06-25 - Prevent eval() for dynamic property access

**Vulnerability:** Found `eval()` being used in `script.py` to evaluate the truthiness of session state variables via strings like `'st.session_state.project'`. This is dangerous as `eval()` executes arbitrary code. While the input in this case was hardcoded, relying on `eval()` is a poor security practice and an anti-pattern.

**Learning:** `eval()` should never be used to check dictionary or object properties. It introduces significant code execution risk if user input ever finds its way into the evaluated string.

**Prevention:** Always use safe dictionary access methods like `st.session_state.get(key)` to retrieve and check values dynamically instead of evaluating string representations of variables.