## 2026-09-26 - Adding Tooltips to Streamlit Action Buttons
**Learning:** Streamlit form submit buttons lack descriptive context by default, making their specific functions (e.g., "Debug" vs "Convert" vs "Execute") potentially ambiguous. Adding the `help` parameter is a highly effective, low-effort way to introduce micro-UX tooltips without cluttering the UI.
**Action:** When working with Streamlit UI files, proactively look for action buttons (`st.form_submit_button`, `st.button`) and apply the `help` parameter to provide immediate, context-sensitive guidance to users.
