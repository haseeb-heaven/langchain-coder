
## 2026-06-18 - [eval() removal for Session State]
**Vulnerability:** Use of eval() to dynamically check string variable names ('st.session_state.project') which can lead to arbitrary code execution if inputs are manipulated.
**Learning:** It existed to simplify checking multiple dynamically named session state variables using a dictionary mapping.
**Prevention:** Use direct dictionary lookups or st.session_state.get('project') instead of executing variable names as strings using eval().
