## 2026-07-13 - [Adding Micro-UX Loading States]
**Learning:** In Streamlit applications, long-running operations (like AI API calls or code compilation) need immediate visual feedback to prevent the user from thinking the app is frozen. Wrapping targeted execution blocks in `with st.spinner("..."):` provides this feedback effectively without requiring large architectural changes.
**Action:** Apply targeted `st.spinner()` wrappers around specific long-running function calls instead of wrapping entire multi-line conditional branches to comply with micro-UX 50-line limits.
