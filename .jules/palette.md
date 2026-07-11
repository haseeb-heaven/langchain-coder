## 2024-05-13 - Adding visual feedback for long-running operations
**Learning:** In Streamlit applications, long-running operations like AI generation or API calls can make the app appear unresponsive.
**Action:** Wrap long-running operations in a `with st.spinner("..."):` block to provide clear, immediate visual feedback to the user. Keep these blocks localized to the specific action rather than wrapping large conditional branches to maintain clean code structure.
