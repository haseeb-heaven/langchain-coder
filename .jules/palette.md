## 2026-08-10 - Added helpful tooltips to Streamlit form buttons
**Learning:** Streamlit form submit buttons lack descriptive context by default. Adding the `help` parameter provides a tooltip that explains the button's action, improving accessibility and usability for users who might need clarification on what each action does without taking up extra screen space.
**Action:** Always add descriptive `help` tooltips to `st.form_submit_button` calls in Streamlit applications.
