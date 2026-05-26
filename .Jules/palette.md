## 2024-05-18 - Streamlit label_visibility and Accessibility
**Learning:** In Streamlit, setting `label_visibility='collapsed'` or `'hidden'` on input elements removes visual clutter but causes them to lose their accessibility context for screen readers.
**Action:** Always provide a descriptive `help` tooltip parameter alongside a `placeholder` when hiding Streamlit input labels to maintain accessibility and provide context.
