## 2026-07-24 - Adding Immediate Visual Feedback
**Learning:** In Streamlit applications, wrapping long-running operations (like AI generation or external API calls) in `with st.spinner("..."):` provides clear, immediate visual feedback to the user, enhancing perceived performance and preventing confusion. Applying this micro-UX change directly to the execution block keeps the modification small (< 50 lines) without needing to wrap large conditional branches.
**Action:** Always add loading spinners to long-running tasks in Streamlit apps for a smoother and more responsive user experience.
