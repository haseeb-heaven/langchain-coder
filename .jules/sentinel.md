## 2024-05-24 - [Remove eval() anti-pattern]
**Vulnerability:** Found `eval()` used dynamically evaluate strings to check values in `st.session_state`.
**Learning:** Using `eval()` can lead to arbitrary code execution if user inputs end up in the evaluated string.
**Prevention:** Never use `eval()` for dictionaries or session state validation. Always use safe lookups like `.get()`.
