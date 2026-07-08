## 2024-05-24 - Streamlit Async Operations Loading States
**Learning:** Long-running operations in Streamlit (like AI generations or external API calls) can cause the UI to appear unresponsive, leading to poor user experience.
**Action:** Always wrap async or long-running execution blocks in `with st.spinner("..."):` to provide immediate, clear visual feedback to the user without blocking UI rendering.
