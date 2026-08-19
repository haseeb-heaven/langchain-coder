## 2026-08-19 - Command Injection Vulnerability
**Vulnerability:** Use of `os.system` with direct shell commands, potentially vulnerable to injection if input were ever parameterized or manipulated.
**Learning:** Python's `os.system` is inherently risky when calling shell commands. It relies on the shell to parse the command string, which can lead to command injection if external input is introduced.
**Prevention:** Always use `subprocess.run` with a list of arguments and `check=True` (or equivalent safe defaults) instead of `os.system`. This avoids the shell entirely and passes arguments directly to the executable, eliminating the risk of shell injection.
