## 2024-06-28 - Missing Visual Feedback for AI Operations
**Learning:** This app frequently calls LLMs (OpenAI, Gemini, Palm, Vertex AI) for code generation and debugging, which are slow, blocking operations. By default, Streamlit provides an obscure "running" indicator in the top right, but it's not contextual or obvious enough.
**Action:** Always wrap long-running operations like AI generation, converting, debugging, and executing code within a `st.spinner("...")` context manager to provide clear, immediate, and descriptive visual feedback to the user on what is currently happening.
