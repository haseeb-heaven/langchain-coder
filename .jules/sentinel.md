## 2026-08-11 - Command Injection via os.system
**Vulnerability:** Found insecure use of `os.system()` with unescaped shell commands in `upgrade_pip_packages()` in `libs/utils.py`.
**Learning:** `os.system()` evaluates commands via the shell, creating a high risk of command injection. In this codebase, it was used to upgrade pip packages, which could be abused if inputs were somehow controlled.
**Prevention:** Always use `subprocess.run()` with a list of arguments and `check=True` to bypass the shell and securely execute external commands.
