# 🤝 Contributing Guide

How to contribute to IRIS and help improve the project.

## Getting Started

### 1. Fork & Clone

```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/IRIS.git
cd IRIS

# Add upstream remote
git remote add upstream https://github.com/HARSHAN-DEVHUB/IRIS.git
```

### 2. Setup Development Environment

```bash
# Create virtual environment
python3 -m venv iris_env
source iris_env/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Verify setup
python scripts/verify_setup.py
```

---

## Development Workflow

### 1. Create Feature Branch

```bash
# Update main branch
git fetch upstream
git checkout main
git rebase upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

**Branch Naming**:
- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation
- `test/description` - Tests
- `refactor/description` - Code improvements

### 2. Make Changes

```bash
# Edit files
vim iris/voice/speech_to_text.py

# Commit frequently with clear messages
git add iris/voice/speech_to_text.py
git commit -m "feat: Add noise filtering to speech recognition"
```

### 3. Code Quality Checks

```bash
# Format code
black .

# Lint code
flake8 . --max-line-length=100

# Type checking
mypy .

# Run tests
pytest tests/ -v --cov=.

# All checks
./scripts/check_quality.sh
```

### 4. Write Tests

```bash
# Create test file
touch tests/test_your_feature.py

# Write tests
cat > tests/test_your_feature.py << 'EOF'
import pytest
from your_module import your_function

def test_your_feature():
    assert your_function() == expected_result

@pytest.mark.integration
def test_feature_integration():
    # Integration test
    pass
EOF

# Run tests
pytest tests/test_your_feature.py -v
```

### 5. Update Documentation

```bash
# If adding new features, update relevant docs
# e.g., if adding command: update docs/COMMANDS.md

nano docs/COMMANDS.md
# Add your command documentation
```

### 6. Commit & Push

```bash
# Stage changes
git add .

# Commit with clear message
git commit -m "feat: Add noise filtering to speech recognition

- Improved audio preprocessing
- Reduces false wake-word detections
- Adds configurable noise threshold
- Includes unit tests

Closes #123"

# Push to your fork
git push origin feature/your-feature-name
```

### 7. Submit Pull Request

1. Go to GitHub and create PR
2. **Title**: Clear, concise description
3. **Description**: Explain what and why
4. **Linked Issues**: Reference with `#123`
5. **Checklist**: Complete the PR template

**PR Template**:
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Enhancement
- [ ] Documentation

## Related Issues
Closes #123

## Testing
- [ ] Unit tests added
- [ ] Integration tests added
- [ ] Manual testing done

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes
```

### 8. Respond to Review

```bash
# Make requested changes
vim iris/voice/speech_to_text.py

# Commit changes
git commit -m "Address review feedback: improve error handling"

# Push changes (same branch)
git push origin feature/your-feature-name

# Do NOT force push unless instructed
```

### 9. Merge & Cleanup

Once approved:
```bash
# Delete local branch
git branch -d feature/your-feature-name

# Delete remote branch
git push origin --delete feature/your-feature-name

# Sync with upstream
git fetch upstream
git checkout main
git rebase upstream/main
```

---

## Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Code style (no logic change)
- `refactor` - Code refactoring
- `test` - Tests
- `chore` - Build, dependencies

**Examples**:
```
feat(voice): Add noise filter to speech recognition

fix(executor): Handle command timeout gracefully

docs(readme): Update installation instructions

refactor(brain): Simplify intent parser logic
```

---

## Code Standards

### Style Guide: PEP 8

```python
# ✓ Good
def process_voice_input(audio_data: bytes) -> str:
    """Process raw audio and return transcription."""
    try:
        result = transcribe(audio_data)
        return result
    except AudioError as e:
        raise AudioProcessingError(f"Failed: {e}")

# ✗ Bad
def processVoiceInput(audio_data):
    result=transcribe(audio_data)
    return result
```

### Type Hints

```python
# ✓ Always use type hints
def listen(timeout: int = 10) -> str:
    pass

# ✗ No type hints
def listen(timeout=10):
    pass
```

### Docstrings

```python
def generate_response(prompt: str, temperature: float = 0.7) -> str:
    """Generate AI response from prompt.
    
    Args:
        prompt: Input text prompt
        temperature: Sampling temperature (0.0-1.0)
        
    Returns:
        Generated response text
        
    Raises:
        LLMError: If LLM is unavailable
    """
    pass
```

---

## Types of Contributions

### Bug Fixes

1. Verify bug with minimal example
2. Add test that reproduces bug
3. Fix the bug
4. Verify test passes
5. Submit PR with reproduction steps

### Features

1. Discuss feature in issue first
2. Create PR with implementation
3. Add comprehensive tests
4. Update documentation
5. Add examples

### Documentation

1. Clarify existing docs
2. Add missing sections
3. Fix typos/grammar
4. Add examples
5. Update API docs

### Tests

1. Add test cases for uncovered code
2. Improve test quality
3. Add integration tests
4. Improve test performance

### Performance

1. Profile to find bottlenecks
2. Optimize with before/after measurements
3. Ensure no behavior changes
4. Document improvements

---

## Testing Requirements

- ✅ All new features must have tests
- ✅ Bug fixes must have regression tests
- ✅ Test coverage ≥ 80%
- ✅ All tests must pass
- ✅ Integration tests for complex flows

```bash
# Before submitting PR
pytest tests/ -v --cov=. --cov-report=html
# Coverage should be ≥ 80%
```

---

## Review Process

1. **Automated Checks**
   - Tests pass
   - Code style valid
   - Type hints correct
   - Coverage maintained

2. **Code Review**
   - Logic review
   - Best practices
   - Performance
   - Documentation

3. **Maintainer Review**
   - Alignment with vision
   - Overall quality

4. **Approval & Merge**
   - Maintainer approves
   - Branch merged

**Response Times**:
- Bug reports: 24-48 hours
- Features: 3-7 days
- PRs: 2-5 days

---

## Common Issues

### "My branch is behind"

```bash
git fetch upstream
git rebase upstream/main
git push origin --force-with-lease
```

### "Merge conflicts"

```bash
# Resolve conflicts in editor
git add .
git rebase --continue
```

### "Tests fail locally"

```bash
# Ensure clean environment
python -m venv test_env
source test_env/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
pytest tests/
```

---

## Getting Help

- 📖 Read [development docs](DEVELOPMENT.md)
- 💬 Ask in [discussions](https://github.com/HARSHAN-DEVHUB/IRIS/discussions)
- 🐛 Check [open issues](https://github.com/HARSHAN-DEVHUB/IRIS/issues)
- 💼 Email: development@iris-assistant.dev

---

## Code of Conduct

- Be respectful
- Welcome newcomers
- Focus on code, not people
- Help others learn
- Report issues privately

---

Thank you for contributing to IRIS! 🎉

See [Testing Guide](TESTING.md) for detailed testing information and [Development Roadmap](DEVELOPMENT.md) for project structure.
