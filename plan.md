1. **Fix `st.toast(traceback.format_exc())`** in `libs/general_utils.py`:
   - Replace it with a secure generic error message to prevent leaking stack traces.
2. **Fix XSS Vulnerability** in `libs/general_utils.py`:
   - Add `import html` and use `html.escape(code_prompt)` in the `generate_dynamic_html` function to prevent unescaped code execution in the generated HTML.
3. **Run Validation and Create Sentinel Journal Entry**:
   - Write a journal entry at `.jules/sentinel.md` recording this vulnerability and its fix.
   - Run python compile tests to ensure no regressions.
4. **Complete Pre-Commit Steps and Submit**:
   - Get instructions from `pre_commit_instructions` to test, verify, review, and reflect.
   - Call submit tool.
