## 2026-05-09 - Adding loading states to long-running Streamlit operations
**Learning:** In Streamlit apps that interface with external LLM APIs (OpenAI, Vertex AI, etc.) or execute remote code, users need immediate visual feedback while waiting. Without this, the UI feels unresponsive.
**Action:** Always use `st.spinner()` as a context manager for code blocks triggered by form submit buttons that perform network requests or long-running computations.
