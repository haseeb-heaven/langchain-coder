## 2026-07-18 - Adding Spinners for Async Actions in Streamlit

**Learning:** Streamlit UI components running synchronous or long-running async tasks block the interface. Without a visual indicator, users may assume the application is unresponsive. Wrapping the execution block directly (e.g. `with st.spinner("..."): `) instead of the whole button conditional branch is a cleaner UX fix that maintains code organization under 50 lines.
**Action:** Always add `st.spinner()` (or equivalent loading states) when initiating long-running code generation or execution actions in Streamlit to improve perceived performance and keep the user informed.
