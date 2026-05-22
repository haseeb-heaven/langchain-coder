## 2024-05-22 - [CRITICAL] Fix eval() vulnerability in dictionary comprehensions
**Vulnerability:** Found arbitrary code execution vulnerability where `eval()` was used to dynamically evaluate strings like "st.session_state.project" to check if variables were set.
**Learning:** Using `eval()` to dynamically check dictionary values or evaluate Python expressions is a critical security anti-pattern that can lead to arbitrary code execution if any part of the string can be influenced by user input.
**Prevention:** Never use `eval()` to check state. Instead, directly access values using safe methods like `dict.get(key)` or `st.session_state.get(key)`.
