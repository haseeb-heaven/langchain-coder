## 2024-05-22 - Streamlit Collapsed Labels Accessibility
**Learning:** In Streamlit UIs, using `label_visibility='collapsed'` on inputs (like `st.text_input`) causes them to lose their accessibility context and label associations, leading to poor UX for screen readers.
**Action:** When a label must be hidden for layout purposes, always compensate by providing a descriptive `help` tooltip and an actionable `placeholder` example to ensure the input's purpose remains clear.
