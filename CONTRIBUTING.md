# Contributing to Resume Keyword Matcher

First off, thank you for considering contributing to Resume Keyword Matcher! It's people like you that make this tool better for everyone.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project and everyone participating in it is governed by respect, professionalism, and inclusivity. By participating, you are expected to uphold this code.

### Our Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

**Bug Report Template:**

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:

1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**

- OS: [e.g. Windows 11, macOS 14, Ubuntu 22.04]
- Python Version: [e.g. 3.13.6, 3.11.5]
- Streamlit Version: [e.g. 1.52.2]
- Browser: [e.g. Chrome 120, Firefox 121]

**Additional context**
Any other context about the problem.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List some examples** of where this enhancement could be used

### Your First Code Contribution

Unsure where to begin? You can start by looking through these issues:

- `good-first-issue` - Issues suitable for beginners
- `help-wanted` - Issues that need extra attention

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/resume-keyword-matcher.git
cd resume-keyword-matcher

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/resume-keyword-matcher.git
```

### 2. Set Up Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows PowerShell
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install black flake8 mypy pytest
```

### 3. Create a Branch

```bash
# Update your fork
git checkout main
git pull upstream main

# Create a feature branch
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

```python
# Good
def analyze_resume(resume_text: str, job_description: str) -> dict:
    """
    Analyze resume against job description.

    Args:
        resume_text: The extracted resume text
        job_description: The job posting text

    Returns:
        Dictionary containing analysis results
    """
    # Implementation
    pass

# Bad
def analyzeResume(resumeText, jobDescription):
    # No docstring, camelCase, no type hints
    pass
```

### Code Formatting

We use [Black](https://github.com/psf/black) for code formatting:

```bash
# Format all Python files
black .

# Check formatting without making changes
black --check .
```

### Type Hints

Use type hints for function parameters and return values:

```python
from typing import Optional, Dict, List, Any

def extract_keywords(text: str, count: int = 10) -> List[str]:
    """Extract top keywords from text."""
    pass

def analyze_data(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Analyze the provided data."""
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of function.

    Longer description if needed, explaining what the function does,
    any important details, edge cases, etc.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When param2 is negative
    """
    pass
```

### Error Handling

Always include appropriate error handling:

```python
# Good
try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    # Handle gracefully
    return None

# Bad
try:
    result = risky_operation()
except:
    pass  # Silent failure
```

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**

```
feat(analyzer): add support for multiple file formats

Add support for analyzing Word documents (.docx) in addition to PDFs.
Includes new utility functions for text extraction.

Closes #123

---

fix(ui): correct score calculation display

The match score was being rounded incorrectly in the UI component.
Changed to use proper rounding function.

Fixes #456

---

docs(readme): update installation instructions

Add troubleshooting section and clarify API key setup process.
```

### Commit Best Practices

- Write clear, descriptive commit messages
- Keep commits atomic (one logical change per commit)
- Reference issues in commit messages when applicable
- Don't commit commented-out code or debug statements
- Don't commit `.env` files or API keys

## Pull Request Process

### Before Submitting

1. **Test your changes**

   ```bash
   # Run the app locally
   streamlit run app.py

   # Test with different scenarios
   # - Various PDF formats
   # - Long/short job descriptions
   # - Edge cases
   ```

2. **Format your code**

   ```bash
   black .
   ```

3. **Check for issues**

   ```bash
   flake8 .
   ```

4. **Update documentation**

   - Update README.md if needed
   - Add/update docstrings
   - Update CHANGELOG.md (if exists)

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: your descriptive message"
   ```

### Submitting the Pull Request

1. **Push to your fork**

   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill out the PR template

### Pull Request Template

```markdown
## Description

Brief description of what this PR does.

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing Done

- [ ] Tested with various PDF formats
- [ ] Tested with different job descriptions
- [ ] Tested UI on mobile/desktop
- [ ] Tested error scenarios
- [ ] Verified no console errors

## Screenshots (if applicable)

Add screenshots to demonstrate the changes.

## Checklist

- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes

## Related Issues

Closes #(issue number)
```

### Review Process

1. At least one maintainer will review your PR
2. Address any feedback or requested changes
3. Once approved, a maintainer will merge your PR
4. Your contribution will be acknowledged in release notes

## Development Tips

### Running in Development Mode

```bash
# Auto-reload on file changes
streamlit run app.py --server.runOnSave true

# Run on specific port
streamlit run app.py --server.port 8502

# Enable debug mode
streamlit run app.py --logger.level debug
```

### Testing Tips

1. **Test with real resumes** - Use various formats and lengths
2. **Test API limits** - Verify handling of rate limits
3. **Test error cases** - Invalid inputs, missing API key, etc.
4. **Test UI responsiveness** - Check mobile and desktop views
5. **Test different browsers** - Chrome, Firefox, Safari, Edge

### Common Development Tasks

```bash
# View logs
streamlit run app.py --logger.level debug

# Clear Streamlit cache
streamlit cache clear

# Generate requirements.txt
pip freeze > requirements.txt

# Check dependencies for security issues
pip-audit
```

## Project Structure

```
resume-keyword-matcher/
├── app.py                    # Main Streamlit app
├── utils/
│   ├── __init__.py
│   ├── pdf_extractor.py      # PDF text extraction
│   ├── gemini_analyzer.py    # Gemini API integration
│   └── report_generator.py   # PDF report generation
├── assets/
│   ├── styles.css            # Custom CSS
│   └── images/               # Image assets
├── tests/                    # Test files (add as needed)
├── .streamlit/
│   └── config.toml           # Streamlit config
├── requirements.txt          # Python dependencies
├── README.md                 # Main documentation
├── CONTRIBUTING.md           # This file
└── LICENSE                   # Project license
```

## Questions?

Feel free to:

- Open an issue with the `question` label
- Reach out to maintainers
- Check existing issues and discussions

## Recognition

Contributors will be:

- Listed in release notes
- Acknowledged in README.md
- Given credit in commit history

Thank you for contributing! 🎉
