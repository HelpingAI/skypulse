<div align="center">

# 🤝 Contributing to SkyPulse

*Thank you for considering contributing to SkyPulse! This document provides guidelines and instructions for contributing.*

</div>

## 📋 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [Getting Started](#-getting-started)
- [Development Setup](#-development-setup)
- [Making Changes](#-making-changes)
- [Testing](#-testing)
- [Pull Request Process](#-pull-request-process)
- [Style Guide](#-style-guide)
- [Community](#-community)

## 📜 Code of Conduct

We are committed to providing a welcoming and inclusive experience for everyone. By participating in this project, you agree to abide by our Code of Conduct.

### Our Standards

- Be respectful and inclusive
- Be patient and welcoming
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

## 🚀 Getting Started

1. **Fork the Repository**
   ```bash
   # Clone your fork
   git clone https://github.com/your-username/skypulse.git
   cd skypulse
   
   # Add upstream remote
   git remote add upstream https://github.com/HelpingAI/skypulse.git
   ```

2. **Stay Updated**
   ```bash
   # Get latest changes
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

## 💻 Development Setup

1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Unix/MacOS:
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   # Install development dependencies
   pip install -e ".[dev]"
   ```

3. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

## 🔄 Making Changes

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write clean, readable code
   - Follow the style guide
   - Add tests for new features
   - Update documentation as needed

3. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```
   
   Follow our commit message convention:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation
   - `test:` for tests
   - `refactor:` for refactoring
   - `style:` for formatting changes
   - `chore:` for maintenance tasks

## 🧪 Testing

1. **Run Tests**
   ```bash
   # Run all tests
   pytest
   
   # Run with coverage
   pytest --cov=skypulse tests/
   
   # Run specific test file
   pytest tests/test_specific.py
   ```

2. **Code Quality Checks**
   ```bash
   # Format code
   black .
   
   # Sort imports
   isort .
   
   # Type checking
   mypy .
   
   # Linting
   ruff check .
   pylint skypulse
   ```

## 📤 Pull Request Process

1. **Update Your Branch**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push Changes**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request**
   - Use a clear, descriptive title
   - Reference any related issues
   - Fill out the PR template
   - Ensure all checks pass

4. **Code Review**
   - Address review comments
   - Make requested changes
   - Keep the PR updated

## 📝 Style Guide

### Python Code Style

- Follow [PEP 8](https://pep8.org/) guidelines
- Use type hints for all functions
- Maximum line length: 88 characters (Black default)
- Use docstrings for all public functions and classes

### Documentation Style

- Use clear, concise language
- Include code examples where appropriate
- Keep headings hierarchical
- Update README.md when needed

### Example Code Style

```python
from typing import Optional, List

def process_data(items: List[str], limit: Optional[int] = None) -> List[str]:
    """Process a list of items with an optional limit.
    
    Args:
        items: List of strings to process
        limit: Optional maximum number of items to process
        
    Returns:
        List of processed strings
    """
    if limit is not None:
        items = items[:limit]
    return [item.strip().lower() for item in items]
```

## 👥 Community

- **Questions?** Open a [Discussion](https://github.com/HelpingAI/skypulse/discussions)
- **Found a Bug?** Submit an [Issue](https://github.com/HelpingAI/skypulse/issues)
- **New Feature?** Discuss in [Issues](https://github.com/HelpingAI/skypulse/issues)

<div align="center">

---

Thank you for contributing to SkyPulse! ❤️

</div>
