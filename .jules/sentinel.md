## 2026-09-21 - [Fix Command Injection Risk]
**Vulnerability:** Use of os.system allows command injection vulnerabilities.
**Learning:** In libs/utils.py, os.system was used for pip upgrade. While hardcoded here, using os.system sets a bad precedent and can lead to vulnerabilities if inputs become dynamic.
**Prevention:** Always use subprocess.run with lists of arguments and check=True instead of os.system to avoid shell injection vulnerabilities.
