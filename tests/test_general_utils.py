import pytest
from libs.general_utils import GeneralUtils

class TestGeneralUtils:
    def setup_method(self):
        self.utils = GeneralUtils()

    def test_extract_code_with_language_specifier(self):
        code = "```python\nprint(1)\n```"
        assert self.utils.extract_code(code) == "print(1)\n"

    def test_extract_code_without_language_specifier(self):
        code = "```\nprint(2)\n```"
        assert self.utils.extract_code(code) == "print(2)\n"

    def test_extract_code_embedded_in_text(self):
        code = "some text before\n```python\nprint(3)\n```\nsome text after"
        assert self.utils.extract_code(code) == "print(3)\n"

    def test_extract_code_no_markdown(self):
        code = "just some code"
        assert self.utils.extract_code(code) == "just some code"

    def test_extract_code_empty_string(self):
        code = ""
        assert self.utils.extract_code(code) == ""

    def test_extract_code_none(self):
        code = None
        assert self.utils.extract_code(code) is None

    def test_extract_code_multiple_blocks(self):
        # Should extract the first block
        code = "```python\nprint(1)\n```\nsome text\n```python\nprint(2)\n```"
        assert self.utils.extract_code(code) == "print(1)\n"

    def test_extract_code_only_backticks(self):
        # Just backticks with no code inside
        code = "```\n```"
        assert self.utils.extract_code(code) == ""

    def test_extract_code_missing_end_backticks(self):
        code = "```python\nprint(1)"
        # It should extract everything after the first newline
        assert self.utils.extract_code(code) == "print(1)"
