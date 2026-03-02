# 🤝 Contributing to FreeLauncher

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the FreeLauncher project.

## 📋 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Respect others' opinions
- Focus on the code, not the person

## 🎯 How to Contribute

### Reporting Bugs

1. Check if the bug has been reported already in [Issues](https://github.com/yourusername/freelauncher/issues)
2. If not, create a new issue with:
   - Clear title
   - Description of the bug
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Python version and OS

### Suggesting Features

1. Check if someone has suggested it in [Discussions](https://github.com/yourusername/freelauncher/discussions)
2. Create a discussion or issue with:
   - Clear description of the feature
   - Use cases
   - Example usage
   - Why it would be useful

### Code Contributions

## 📚 Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/freelauncher.git
   cd freelauncher
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: .\venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov black flake8 mypy
   ```

4. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

## 🛠️ Development Workflow

### Code Style

We follow PEP 8 with some customizations:

- Line length: 100 characters
- Use type hints for all functions
- Write docstrings for all classes and functions
- Use meaningful variable names

### Format Code

```bash
black src/
```

### Run Linter

```bash
flake8 src/
```

### Type Checking

```bash
mypy src/
```

### Run Tests

```bash
pytest tests/ -v --cov=src
```

### All Checks

```bash
python setup.py all
```

## 📝 Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Build process or dependencies

### Examples

```
feat(profiles): add profile description field
fix(launcher): handle missing Java installation
docs(readme): update installation instructions
test(profile_manager): add validation tests
```

### Commit Message Rules

- ✅ Use imperative mood ("add feature" not "added feature")
- ✅ Don't capitalize first letter
- ✅ No period at the end
- ✅ Limit subject to 50 characters
- ✅ Wrap body at 72 characters
- ✅ Reference issues: `fixes #123`

## 🧪 Testing

### Write Tests for New Features

- Place tests in `tests/` directory
- Name files `test_*.py`
- Use `unittest` or `pytest`
- Test happy path and error cases
- Aim for >80% code coverage

### Example Test

```python
import unittest
from src.core.profile_manager import Profile, InvalidProfileError

class TestProfile(unittest.TestCase):
    def test_valid_profile(self):
        profile = Profile(name="Test", username="Steve", ram=4)
        self.assertEqual(profile.name, "Test")
    
    def test_invalid_profile(self):
        with self.assertRaises(InvalidProfileError):
            Profile(name="", username="Steve", ram=4)
```

### Run Specific Tests

```bash
pytest tests/test_profiles.py -v
pytest tests/test_profiles.py::TestProfile::test_valid_profile -v
```

## 📝 Writing Documentation

- Update README.md if adding features
- Add docstrings to all functions/classes
- Update MIGRATION.md if changing APIs
- Use clear, concise language
- Include code examples

### Docstring Format

```python
def create_profile(self, name: str, username: str, ram: int) -> Profile:
    """
    Create a new profile.
    
    Args:
        name: Profile name (must be unique)
        username: Minecraft username
        ram: RAM allocation in GB (1-32)
    
    Returns:
        Created Profile object
    
    Raises:
        ProfileAlreadyExistsError: If profile already exists
        InvalidProfileError: If profile data is invalid
    """
```

## 🔄 Pull Request Process

1. **Ensure your code is ready**
   ```bash
   python setup.py all
   ```

2. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat(feature): describe your changes"
   ```

3. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

4. **Create a Pull Request**
   - Go to GitHub and create a PR
   - Fill in the PR template
   - Reference related issues: `fixes #123`
   - Describe what changes and why

5. **PR Guidelines**
   - ✅ All tests pass
   - ✅ Code is formatted with black
   - ✅ No flake8 warnings
   - ✅ Type hints added
   - ✅ Docstrings written
   - ✅ Documentation updated
   - ✅ Related issues referenced

### PR Template

```markdown
## Description
Brief description of changes

## Related Issues
Closes #(issue number)

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation

## Testing
Describe testing done

## Checklist
- [ ] Code formatted (black)
- [ ] Tests pass (pytest)
- [ ] No lint issues (flake8)
- [ ] Type hints added (mypy)
- [ ] Docstrings updated
- [ ] Documentation updated
```

## 🏗️ Architecture Guidelines

### SOLID Principles

- **S**ingle Responsibility: One responsibility per class
- **O**pen/Closed: Open for extension, closed for modification
- **L**iskov Substitution: Subtypes are substitutable
- **I**nterface Segregation: Clients depend on specific interfaces
- **D**ependency Inversion: Depend on abstractions, not concretions

### Module Organization

```
src/
├── core/          # Business logic (no UI dependencies)
├── ui/            # User interface (can depend on core)
└── utils/         # Shared utilities (no dependencies)
```

### When Adding Features

1. Determine which module it belongs to
2. Write tests first (TDD)
3. Implement the feature
4. Update documentation
5. Request review

## 🐛 Debugging Tips

### Enable Debug Logging

Edit `src/utils/config.py`:
```python
LOG_LEVEL = "DEBUG"
```

### Check Logs

```bash
tail -f ~/.freelauncher/logs/freelauncher_*.log
```

### Use Python Debugger

```python
import pdb; pdb.set_trace()
```

## 📚 Resources

- [Python PEP 8](https://pep8.org/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [SOLID Principles](https://www.digitalocean.com/community/conceptual_articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

## ❓ Questions?

- Open an issue
- Start a discussion
- Contact maintainers

---

Thank you for contributing to FreeLauncher! 🚀
