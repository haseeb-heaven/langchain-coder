import pytest
from libs.general_utils import GeneralUtils

def test_generate_dynamic_html_valid():
    utils = GeneralUtils()
    html = utils.generate_dynamic_html('Python', 'print("Hello World")')
    assert 'data-language="python"' in html
    assert 'print("Hello World")' in html

def test_generate_dynamic_html_invalid_language():
    utils = GeneralUtils()
    with pytest.raises(KeyError):
        utils.generate_dynamic_html('InvalidLanguage', 'print("Hello World")')
