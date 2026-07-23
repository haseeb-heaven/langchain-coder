## 2026-07-23 - Added loading indicators for async operations
**Learning:** Synchronous execution of AI API calls freezes the Streamlit UI, degrading user experience. Wrapping targeted execution blocks with 'st.spinner()' provides immediate visual feedback.
**Action:** Apply 'with st.spinner("...");' to all async operations (Debug, Convert, Execute) rather than indenting large multi-line conditional branches to keep changes targeted.
