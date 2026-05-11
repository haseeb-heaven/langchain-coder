## 2026-05-11 - Streamlit Spinners
**Learning:** Long-running LLM generation and validation calls in Streamlit UI feel unresponsive without explicit loading indicators.
**Action:** Use `st.spinner('message')` as a context manager around any long-running actions (e.g., code generation, execution, API calls) to provide immediate visual feedback to the user.
