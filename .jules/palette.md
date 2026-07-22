## 2026-07-22 - Added visual feedback for long-running operations
**Learning:** Long-running operations like compiling or API calls can make the app appear frozen. Providing visual feedback using `st.spinner()` significantly improves perceived performance and UX. To minimize code diffs and avoid indenting large conditional branches, it is best applied tightly around the specific execution calls.
**Action:** Wrap long-running calls in Streamlit with `with st.spinner("..."):` to ensure users know an action is in progress.
