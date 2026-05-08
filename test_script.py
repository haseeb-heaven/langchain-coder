import os
import pytest
from unittest.mock import patch, MagicMock

# Import modules and functions from script.py
from script import (
    detect_language,
    check_language_runtime,
    LANGUAGE_REGISTRY,
    LLMClient,
    Config,
    load_config,
    BaseAgent,
    AgentState
)

def test_detect_language_python():
    assert detect_language("Write a python script to add two numbers.") == "python"
    assert detect_language("Create a django web app.") == "python"

def test_detect_language_javascript():
    assert detect_language("Create a javascript function.") == "javascript"
    assert detect_language("Using node.js, write an API.") == "javascript"

def test_detect_language_typescript():
    assert detect_language("Write a ts script.") == "typescript"

def test_detect_language_go():
    assert detect_language("Write a golang server.") == "go"
    assert detect_language("Create a go routine.") == "go"

def test_detect_language_fallback():
    assert detect_language("Write a script to calculate primes.") == "python"

def test_detect_language_hint():
    assert detect_language("Write a web server", hint="rust") == "rust"

def test_llm_client_clean():
    # Test stripping markdown fences
    assert LLMClient._clean("```python\nprint('hello')\n```") == "print('hello')"
    assert LLMClient._clean("```\nprint('hello')\n```") == "print('hello')"
    assert LLMClient._clean("print('hello')") == "print('hello')"
    assert LLMClient._clean("```javascript\nconsole.log('test')```") == "console.log('test')"

@patch.dict(os.environ, {"LLM_MODEL": "gpt-4", "OPENAI_API_KEY": "fake_key"})
def test_load_config_valid():
    config = load_config()
    assert config.model_fleet == [("gpt-4", "fake_key")]
    assert config.max_iterations == 5
    assert config.timeout == 60

@patch.dict(os.environ, clear=True)
def test_load_config_invalid():
    with pytest.raises(ValueError, match="No LLM model configured"):
        load_config()

def test_check_language_runtime():
    # python checker should be available
    spec = LANGUAGE_REGISTRY["python"]
    assert check_language_runtime(spec) is True

    # modify checker to a non-existent binary
    spec_fake = LANGUAGE_REGISTRY["python"]
    old_checker = spec_fake.checker
    spec_fake.checker = "fake_nonexistent_binary_xyz"
    assert check_language_runtime(spec_fake) is False
    spec_fake.checker = old_checker # restore

def test_base_agent_run_cmd():
    config = Config(model_fleet=[("gpt-4", "key")])
    agent = BaseAgent(config)
    result = agent._run_cmd(["echo", "hello"])
    assert result.returncode == 0
    assert result.stdout.strip() == "hello"

def test_base_agent_run_cmd_timeout():
    config = Config(model_fleet=[("gpt-4", "key")], timeout=1)
    agent = BaseAgent(config)
    result = agent._run_cmd(["sleep", "2"])
    assert result.returncode == 1
    assert "timed out" in result.stderr.lower()
