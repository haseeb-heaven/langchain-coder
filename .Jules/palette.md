## 2026-06-04 - Enhance Streamlit Input Accessibility
**Learning:** When using `label_visibility='collapsed'` or `'hidden'` in Streamlit to save UI space, inputs lose accessibility context for screen readers.
**Action:** Always provide a descriptive `help` tooltip and an actionable `placeholder` example to compensate for the missing visible label.
