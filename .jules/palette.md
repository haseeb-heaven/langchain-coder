## 2026-06-30 - Add Spinner for Long-Running Operations
**Learning:** In Streamlit applications, wrap long-running operations (such as AI generation or API calls) in a `with st.spinner("..."):` block to provide clear, immediate visual feedback to the user.
**Action:** Always wrap backend execution calls triggered by buttons in a spinner.
