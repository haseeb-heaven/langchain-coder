## 2026-08-17 - Add Tooltips to Streamlit Buttons
**Learning:** In Streamlit apps, `st.form_submit_button` elements lack context for screen readers and sighted users. Adding the `help` parameter acts as both a tooltip and accessible description.
**Action:** Always use the `help` parameter on Streamlit buttons to improve accessibility and provide micro-guidance without cluttering the UI.
