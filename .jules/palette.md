## 2026-06-26 - Accessibility context lost with hidden labels
**Learning:** In Streamlit UI, inputs using `label_visibility='collapsed'` or `'hidden'` lose accessibility context for screen readers.
**Action:** Compensate by providing descriptive `help` tooltips and actionable `placeholder` examples.
## 2026-10-16 - Native Tooltip Pattern for Density

**Learning:** Streamlit's sidebar layout restricts horizontal space, making descriptive labels difficult. Leveraging the built-in `help` parameter across standard components (sliders, checkboxes, selectboxes) provides an effective, space-saving pattern for adding accessibility context without breaking the dense layout constraint.
**Action:** Consistently apply the `help` parameter to inputs in confined layouts like sidebars to maintain visual density while ensuring functionality remains accessible and discoverable.
