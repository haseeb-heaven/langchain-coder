1. **Add `help` tooltips and actionable `placeholder`s to Streamlit inputs**
   - Modify `script.py` to add `help` text and descriptive placeholders to `st.text_area` and `st.text_input` elements that use `label_visibility='hidden'` or `'collapsed'`, compensating for lost accessibility context.
   - Specifically target `code_prompt`, `code_input`, `code_output`, `code_fix_instructions`, and `code_file` using `replace_with_git_merge_diff`.
2. **Create UX journal entry**
   - Create `.Jules/palette.md` (and the directory) to document the critical learning about `label_visibility` accessibility in Streamlit.
3. **Verify the syntax**
   - Run `python3 -m py_compile script.py` to ensure the Python code has correct syntax.
   - Run `cat .Jules/palette.md` to verify the journal entry creation.
4. **Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.**
   - Run `pre_commit_instructions` and follow the steps.
5. **Submit the change**
   - Commit and submit the code with a descriptive commit message formatted for Palette PRs.
