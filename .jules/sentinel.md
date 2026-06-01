## 2024-05-24 - Insecure Session State Evaluation
**Vulnerability:** Use of `eval()` to dynamically evaluate hardcoded `st.session_state` string keys.
**Learning:** Evaluating code strings to dynamically check dictionary values or state variables is an anti-pattern that can lead to arbitrary code execution if inputs become user-controlled.
**Prevention:** Use direct dictionary lookups or safer alternatives like `st.session_state.get(key)`. Never use `eval()` to check state.
