## 2026-08-05 - [Add tooltips to Streamlit form buttons]
**Learning:** In Streamlit applications, `st.form_submit_button` doesn't natively provide clear context on hover by default, which can leave users unsure about complex AI actions. Adding the `help` parameter serves as an effective tooltip pattern for providing this context without cluttering the UI.
**Action:** Always utilize the `help` parameter on core interaction buttons (especially in forms) to provide immediate, contextual guidance for users.
