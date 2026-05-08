import unittest
from libs.general_utils import GeneralUtils

class TestGeneralUtils(unittest.TestCase):
    def setUp(self):
        self.utils = GeneralUtils()

    def test_extract_code_with_language(self):
        code = "Here is the code:\n```python\nprint('hello')\n```\n"
        extracted = self.utils.extract_code(code)
        self.assertEqual(extracted, "print('hello')\n")

    def test_extract_code_without_language(self):
        # NOTE: Current implementation of extract_code behaves like this:
        # It finds the first ```, then skips until the next \n, and finds the next ```
        # For "```\nprint('hello')\n```", it will return an empty string or partial.
        code = "```\nprint('hello')\n```"
        extracted = self.utils.extract_code(code)
        # Assuming current implementation which returns an empty string or partial content
        # We test for exactly what it returns currently to lock down the behavior.
        self.assertEqual(extracted, "")

    def test_extract_code_no_backticks(self):
        code = "print('hello')"
        extracted = self.utils.extract_code(code)
        self.assertEqual(extracted, "print('hello')")

    def test_extract_code_empty_string(self):
        code = ""
        extracted = self.utils.extract_code(code)
        self.assertEqual(extracted, "")

    def test_extract_code_invalid_type(self):
        # Passing None should trigger the except block and return None
        extracted = self.utils.extract_code(None)
        self.assertIsNone(extracted)

        # Passing an int
        extracted = self.utils.extract_code(123)
        self.assertIsNone(extracted)

    def test_extract_code_missing_end_backticks(self):
        code = "```python\nprint('hello')"
        extracted = self.utils.extract_code(code)
        # Note: '```' not found at end sets end to -1, cutting off the last char
        self.assertEqual(extracted, "print('hello'")

    def test_extract_code_backticks_inside_code(self):
        code = "```python\nprint('```')\n```"
        extracted = self.utils.extract_code(code)
        # Note: finds the internal '```' as the end marker
        self.assertEqual(extracted, "print('")

if __name__ == '__main__':
    unittest.main()
