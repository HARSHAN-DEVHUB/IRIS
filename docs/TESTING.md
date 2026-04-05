# 🧪 Testing Guide

Comprehensive testing guide for IRIS development.

## Running Tests

### Install Test Dependencies

```bash
pip install -r requirements-dev.txt
```

### Run All Tests

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=. --cov-report=html

# Run specific test file
pytest tests/test_voice.py -v

# Run specific test function
pytest tests/test_voice.py::test_speech_to_text -v
```

### Test Categories

```bash
# Run only unit tests
pytest tests/ -m unit

# Run only integration tests
pytest tests/ -m integration

# Run only slow tests (large models)
pytest tests/ -m slow

# Skip slow tests
pytest tests/ -m "not slow" -v
```

### Test Selection

```bash
# Run tests matching pattern
pytest -k "voice" tests/

# Run tests NOT matching pattern
pytest -k "not integration" tests/

# Run first 5 tests then stop
pytest tests/ --maxfail=5
```

---

## Test Structure

### Example Unit Test

```python
# tests/test_voice.py
import pytest
from voice.speech_to_text import VoiceProcessor

@pytest.fixture
def processor():
    """Fixture: Create processor for testing"""
    return VoiceProcessor(test_mode=True)

def test_speech_to_text(processor):
    """Test speech-to-text conversion"""
    # Arrange
    audio_file = "fixtures/sample_audio.wav"
    expected = "open slack"
    
    # Act
    result = processor.transcribe_file(audio_file)
    
    # Assert
    assert result.lower() == expected

def test_text_to_speech(processor):
    """Test text-to-speech"""
    # Should not raise exception
    processor.speak("Hello world")

@pytest.mark.slow
def test_full_voice_loop(processor):
    """Integration: test complete voice cycle"""
    # This test takes longer (marked slow)
    pass
```

### Example Integration Test

```python
# tests/test_integration.py
import pytest
from voice.speech_to_text import VoiceProcessor
from brain.llm_interface import LLMInterface
from executor.command_handler import CommandExecutor

@pytest.mark.integration
def test_end_to_end_command():
    """Test complete command flow"""
    # Setup
    voice = VoiceProcessor(test_mode=True)
    brain = LLMInterface()
    executor = CommandExecutor()
    
    # Simulate: "Open Chrome"
    command = "open chrome"
    intent = brain.parse_intent(command)
    result = executor.execute(intent["action"], intent.get("params", {}))
    
    assert result["status"] == "success"
```

---

## Coverage Report

```bash
# Generate HTML coverage report
pytest tests/ --cov=. --cov-report=html

# Open report
open htmlcov/index.html

# Show coverage in terminal
pytest tests/ --cov=. --cov-report=term-missing

# Target coverage by file
pytest tests/ --cov=. --cov-report=term:skip-covered
```

### Coverage Goals

| Component | Target | Current |
|-----------|--------|---------|
| Voice module | 90% | 85% |
| Brain module | 85% | 80% |
| Executor module | 80% | 75% |
| Security module | 95% | 90% |
| Utils module | 75% | 70% |
| **Overall** | **85%** | **80%** |

---

## Test Fixtures

### Audio Fixtures

```python
# tests/conftest.py
import pytest

@pytest.fixture
def sample_audio():
    """Sample audio file for testing"""
    return "tests/fixtures/sample_audio.wav"

@pytest.fixture
def test_audio_data():
    """Raw audio data for testing"""
    return b'\x00\x01\x02...'  # Raw bytes
```

### Mock Objects

```python
from unittest.mock import Mock, patch

# Mock OpenAI API
@patch('brain.llm_interface.OpenAI')
def test_with_mock_llm(mock_openai):
    mock_openai.return_value.chat.completions.create.return_value = \
        Mock(choices=[Mock(message=Mock(content="response"))])
    
    llm = LLMInterface(provider="openai")
    result = llm.generate("test prompt")
    
    assert "response" in result
```

---

## Performance Testing

```bash
# Profile code execution
python scripts/performance_test.py

# Benchmark critical operations
pytest tests/ --benchmark
```

### Example Performance Test

```python
import pytest

@pytest.mark.benchmark
def test_llm_inference_speed(benchmark):
    """Benchmark LLM inference time"""
    from brain.llm_interface import LLMInterface
    
    llm = LLMInterface()
    
    # Should complete in < 10 seconds
    result = benchmark(llm.generate, "What is Python?")
    assert len(result) > 0
```

---

## Debugging Tests

### Verbose Output

```bash
# Show print statements
pytest tests/ -v -s

# Show local variables on failure
pytest tests/ -vv -l

# Drop into debugger on failure
pytest tests/ --pdb

# Drop into debugger on first error
pytest tests/ --pdbcls=IPython.terminal.debugger:TerminalPdb
```

### Logging During Tests

```python
def test_with_logging(caplog):
    """Test with logging capture"""
    import logging
    
    logger = logging.getLogger(__name__)
    logger.info("Test message")
    
    assert "Test message" in caplog.text
```

---

## Continuous Integration

### GitHub Actions Example

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11, 3.12]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: pytest tests/ --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

---

## Test Checklist

Before submitting PR:

- [ ] All tests pass: `pytest tests/ -v`
- [ ] Coverage ≥ 80%: `pytest tests/ --cov=.`
- [ ] No linting errors: `flake8 .`
- [ ] Code formatted: `black .`
- [ ] Type hints valid: `mypy .`
- [ ] Docstrings present
- [ ] New tests for new features
- [ ] Integration tests for complex flows

---

## Common Issues

### Issue: "ModuleNotFoundError: No module named 'iris'"

```bash
# Install in development mode
pip install -e .
```

### Issue: Tests pass locally but fail in CI

```bash
# Test in isolated environment
python -m venv test_env
source test_env/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
pytest tests/
```

### Issue: Slow tests timeout

```bash
# Skip slow tests during development
pytest tests/ -m "not slow"

# Or increase timeout
pytest tests/ --timeout=300
```

---

See [Contributing](CONTRIBUTING.md) for testing requirements when submitting PRs.
