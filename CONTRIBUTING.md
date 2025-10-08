# Contributing to Grasshopper Quality Analyzer

First off, thank you for considering contributing to Grasshopper Quality Analyzer! 🎉

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

### Our Standards

**Examples of behavior that contributes to a positive environment:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community

**Unacceptable behavior includes:**
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

---

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title**: Descriptive summary of the issue
- **Steps to reproduce**: Detailed steps to reproduce the behavior
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Environment**: 
  - Rhino version
  - Grasshopper version
  - Python version (for MCP)
  - OS version
- **Screenshots**: If applicable
- **Additional context**: Any other relevant information

**Template:**
```markdown
**Description:**
Brief description of the bug

**Steps to Reproduce:**
1. Open Grasshopper
2. Add component...
3. See error

**Expected Behavior:**
Should show...

**Actual Behavior:**
Shows error...

**Environment:**
- Rhino 8.0
- Windows 11
- Python 3.11
```

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:

- **Clear title**: Descriptive summary
- **Use case**: Why is this enhancement needed?
- **Proposed solution**: How should it work?
- **Alternatives considered**: Other approaches you've considered
- **Priority**: How important is this to you?

### Pull Requests

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Development Setup

### Standalone Version

```bash
# 1. Clone the repository
git clone https://github.com/dongwoosuk/grasshopper-quality-analyzer
cd grasshopper-quality-analyzer

# 2. Test in Grasshopper
# - Open Rhino/Grasshopper
# - Add Python component
# - Copy code from standalone/component_*.py
# - Test changes
```

### MCP Version

```bash
# 1. Clone the repository
git clone https://github.com/dongwoosuk/grasshopper-quality-analyzer
cd grasshopper-quality-analyzer/mcp

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run tests (when available)
python -m pytest tests/

# 5. Test your changes
python mcp_server.py
```

---

## Pull Request Process

### Before Submitting

- [ ] Code follows project style guidelines
- [ ] Comments added for complex logic
- [ ] Documentation updated (if needed)
- [ ] No breaking changes (or clearly documented)
- [ ] Tested locally

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How has this been tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests pass
```

### Review Process

1. Maintainer will review your PR
2. Feedback will be provided if changes needed
3. Once approved, PR will be merged
4. Your contribution will be recognized in CHANGELOG

---

## Style Guidelines

### Python Code Style

Follow [PEP 8](https://pep8.org/) with these specifics:

**Naming:**
```python
# Classes: PascalCase
class GHAnalyzer:
    pass

# Functions/Variables: snake_case
def analyze_definition():
    component_count = 0

# Constants: UPPER_SNAKE_CASE
MAX_COMPONENTS = 1000
```

**Documentation:**
```python
def analyze_components(components: List[Dict]) -> Dict:
    """
    Analyze list of components and return statistics
    
    Args:
        components: List of component dictionaries
        
    Returns:
        Dictionary with analysis results
        
    Example:
        >>> analyze_components([{...}])
        {'total': 10, 'errors': 2}
    """
    pass
```

**Imports:**
```python
# Standard library
import os
import sys
from typing import List, Dict

# Third party
from mcp.server import Server

# Local
from analyzer import GHAnalyzer
```

### Grasshopper Python (Standalone)

- Compatible with Python 2.7 (GH Python)
- Avoid f-strings (use .format())
- Test in actual Grasshopper environment
- Keep components self-contained
- Add clear docstrings at top

```python
"""
Component Name - Brief Description

Inputs:
- x: Description
- y: Description

Outputs:
- a: Description
"""
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): subject

body (optional)

footer (optional)
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Tests
- `chore`: Maintenance

**Examples:**
```
feat(analyzer): add plugin dependency detection
fix(standalone): resolve path detection on Windows
docs(readme): update installation instructions
```

---

## Adding New Features

### New Lint Rule

1. Add rule to `mcp/analyzer/lint_rules.py`:
```python
LINT_RULES = {
    "your_rule": {
        "id": "GH0XX",
        "severity": "error|warning|info",
        "title": "Rule Title",
        "description": "What it checks",
        "why_it_matters": "Why it's important",
        "how_to_fix": "How to fix it"
    }
}
```

2. Implement check in `mcp/analyzer/gh_linter.py`:
```python
def check_your_rule(self):
    """Check for your rule"""
    issues = []
    # Your check logic
    return issues
```

3. Add test case (when test suite exists)
4. Update documentation

### New Analysis Feature

1. Add method to `GHAnalyzer` class
2. Update report generation
3. Add to MCP server tools if needed
4. Update documentation
5. Test with sample files

---

## Testing

### Manual Testing Checklist

**Standalone:**
- [ ] Works in Grasshopper
- [ ] Correct output format
- [ ] Handles errors gracefully
- [ ] Performance acceptable

**MCP:**
- [ ] Server starts without errors
- [ ] All tools work correctly
- [ ] Proper error handling
- [ ] JSON format correct

### Test Files

When contributing, please test with:
- Simple definitions (< 50 components)
- Medium definitions (50-200 components)
- Large definitions (200+ components)
- Edge cases (empty, corrupted, etc.)

---

## Documentation

### What Needs Documentation

- New features
- API changes
- Breaking changes
- Configuration options
- Usage examples

### Where to Document

- **README.md**: Overview, quick start
- **docs/**: Detailed guides
- **Code comments**: Implementation details
- **CHANGELOG.md**: Version history

---

## Questions?

- 📧 Email: dongwoosuk0219@gmail.com
- 💬 GitHub Discussions: [Ask a question](https://github.com/dongwoosuk/grasshopper-quality-analyzer/discussions)
- 🐛 GitHub Issues: [Report a bug](https://github.com/dongwoosuk/grasshopper-quality-analyzer/issues)

---

## Recognition

Contributors will be:
- Listed in CHANGELOG
- Mentioned in release notes
- Added to contributors list (when created)

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🦗✨
