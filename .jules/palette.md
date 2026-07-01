## 2024-05-24 - Add spinners to long-running operations
**Learning:** Streamlit applications can appear frozen during long-running AI generation or API calls if there's no visual feedback. Wrapping these operations in `with st.spinner("..."):` provides immediate visual feedback to the user, significantly improving the perceived responsiveness and overall user experience.
**Action:** Always wrap long-running backend or API operations in a visual loading indicator (like `st.spinner`) in Streamlit applications.
