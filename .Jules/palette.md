## 2024-05-08 - Added Visual Loading Indicators
**Learning:** During long-running AI API calls or code compilation in Streamlit apps, the lack of immediate visual feedback makes the interface feel unresponsive. Users might repeatedly click buttons or wonder if the app is frozen.
**Action:** Always wrap long-running operations triggered by buttons (like AI generation or external API calls) with `with st.spinner("..."):` in Streamlit apps to provide immediate, clear feedback.
