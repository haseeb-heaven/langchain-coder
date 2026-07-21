## 2026-07-21 - Adding Immediate Feedback to Streamlit Actions
**Learning:** In Streamlit applications, long-running operations (like API calls) freeze the application without giving visual feedback, leading to a poor experience. Complex conditional branches make it difficult to wrap large sections in `st.spinner`.
**Action:** Apply `with st.spinner("..."):` selectively to targeted execution blocks to keep micro-UX changes under 50 lines while providing immediate visual feedback to the user.
