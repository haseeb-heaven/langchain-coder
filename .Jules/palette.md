## 2024-05-18 - Visual Feedback for AI Operations
**Learning:** In AI code generation applications built with Streamlit, executing network requests to language models and running compilers can introduce significant delays where the UI appears frozen or unresponsive to users.
**Action:** Always wrap long-running Streamlit operations (like AI completion/generation, API calls, and code execution) with `with st.spinner("...")` to provide immediate, clear visual feedback and reassure the user that the system is processing their request.
