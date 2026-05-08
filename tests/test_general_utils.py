import pytest
from unittest.mock import MagicMock
import sys

# Mock dependencies that might be missing or cause issues
sys.modules['streamlit'] = MagicMock()
sys.modules['requests'] = MagicMock()
sys.modules['google.oauth2'] = MagicMock()
sys.modules['google.auth'] = MagicMock()
sys.modules['google.auth.transport'] = MagicMock()

from libs.general_utils import GeneralUtils

class TestGeneralUtils:
    def setup_method(self):
        self.utils = GeneralUtils()

    def test_calculate_code_generation_cost_basic(self):
        test_string = "a" * 1000
        cost, cost_per_whole_string, total_cost = self.utils.calculate_code_generation_cost(test_string)
        assert cost == 0.0005
        assert cost_per_whole_string == 0.0005
        assert total_cost == 0.0005

    def test_calculate_code_generation_cost_multiple_words(self):
        test_string = ("a " * 500).strip()
        # words = 500
        # letters = 999
        # cost = 0.0005
        # cost_per_whole_string = 0.0005 * (999/1000) = 0.0004995
        # total_cost = 0.0004995

        cost, cost_per_whole_string, total_cost = self.utils.calculate_code_generation_cost(test_string)
        assert cost == 0.0005
        assert pytest.approx(cost_per_whole_string) == 0.0004995
        assert pytest.approx(total_cost) == 0.0004995

    def test_gpt_4_generation_cost(self):
        test_string = "a" * 1000
        cost, cost_per_whole_string, total_cost = self.utils.gpt_4_generation_cost(test_string)
        assert cost == 0.06
        assert total_cost == 0.06

    def test_gpt_3_5_turbo_no_typo(self):
        test_string = "a" * 1000
        cost, cost_per_whole_string, total_cost = self.utils.gpt_3_5_turbo_generation_cost(test_string)
        assert cost == 0.008
        assert total_cost == 0.008

    def test_gemini_pro_generation_cost(self):
        test_string = "a" * 1000
        cost, cost_per_whole_string, total_cost = self.utils.gemini_pro_generation_cost(test_string)
        assert cost == 0.00025
        assert total_cost == 0.00025
