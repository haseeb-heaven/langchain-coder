## 2026-08-11 - Adding Tooltips to Streamlit Form Submit Buttons
**Learning:** Streamlit form submit buttons lack descriptive tooltips by default, which can obscure their precise function, especially for users relying on context. Adding a 'help' parameter provides a quick and accessible tooltip that enhances usability without cluttering the UI.
**Action:** When creating 'st.form_submit_button' instances, always include a descriptive 'help' string to explain the button's action.
