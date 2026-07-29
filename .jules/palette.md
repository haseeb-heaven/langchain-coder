## 2026-07-29 - Added Tooltips to Form Submit Buttons
**Learning:** Streamlit form submit buttons lack descriptive tooltips by default, which can impact usability and accessibility when the button label alone isn't fully explanatory. Adding the `help` parameter to `st.form_submit_button` provides native tooltips as a quick, low-effort micro-UX improvement.
**Action:** Consistently use the `help` parameter on key interactive elements like `st.form_submit_button` and `st.button` in Streamlit applications to provide context and improve the overall user experience.
