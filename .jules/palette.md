## 2026-06-26 - Accessibility context lost with hidden labels
**Learning:** In Streamlit UI, inputs using `label_visibility='collapsed'` or `'hidden'` lose accessibility context for screen readers.
**Action:** Compensate by providing descriptive `help` tooltips and actionable `placeholder` examples.
## 2026-10-11 - Added tooltips to core configuration inputs
**Learning:** Core configuration inputs often lack sufficient context for new users, leading to confusion about what settings do (like compiler mode vs AI option). Built-in framework features like Streamlit's `help` parameter provide a non-intrusive way to offer this context via native tooltips without cluttering the UI.
**Action:** Consistently utilize the `help` parameter on key configuration inputs across the application to provide immediate, contextual guidance.
