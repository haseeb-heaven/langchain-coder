## 2026-08-13 - Added helpful tooltips to form action buttons
**Learning:** In Streamlit, adding `help` parameters to `st.form_submit_button` provides native, accessible tooltips on hover. This is an effective way to clarify the specific behavior of action buttons without cluttering the UI with additional text.
**Action:** Always consider adding `help` text to main action buttons in Streamlit applications, especially when the button label alone might be slightly ambiguous (e.g., "Example" vs. "Load random example prompt").
