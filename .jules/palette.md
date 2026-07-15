## 2026-07-15 - Adding Immediate Loading States
**Learning:** Streamlit applications lack visual feedback during long-running background tasks like AI generation or executing code, leaving users uncertain if the app is responsive or hung.
**Action:** Wrap targeted, long-running execution statements (like API calls or compilations) in `with st.spinner("..."): ` blocks to provide immediate visual loading states, keeping changes under 50 lines by wrapping localized blocks instead of large conditional branches.
