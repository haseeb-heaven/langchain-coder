## 2026-07-04 - Adding Spinners for Async Actions
**Learning:** AI generation and conversion tasks take time, leaving the user without immediate feedback if no loading state is shown. Adding `st.spinner` provides immediate visual confirmation of the background process.
**Action:** Always wrap long-running Streamlit operations (like AI generation or API calls) in a `with st.spinner(...):` block to improve perceived performance and keep users informed.
