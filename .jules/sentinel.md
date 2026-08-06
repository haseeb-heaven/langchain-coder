## 2026-08-06 - Prevent Command Injection
**Vulnerability:** Use of os.system() to execute shell commands with potentially unsanitized arguments.
**Learning:** os.system() is prone to command injection and insecure.
**Prevention:** Always use subprocess.run() with a list of arguments and set check=True to handle errors safely.
