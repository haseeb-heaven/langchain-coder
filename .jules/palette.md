## 2026-07-16 - Adding Visual Feedback to Asynchronous Form Submissions
**Learning:** In Streamlit applications, synchronous form submission handlers (e.g., waiting for AI generation, debugging, or execution) block the UI without visual indication, making the app feel unresponsive.
**Action:** Always wrap potentially long-running or external API calls triggered by form buttons within a `with st.spinner("..."):` block to provide immediate visual feedback.
