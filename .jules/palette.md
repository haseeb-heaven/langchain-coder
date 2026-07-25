## 2026-07-25 - Add Loading States to Actions
**Learning:** Long-running operations like debugging, converting, and executing code in Streamlit block the UI and leave the user uncertain if the app is responsive.
**Action:** Wrap these multi-step/API-driven operations in `with st.spinner("..."):` to provide immediate, clear visual feedback to the user.
