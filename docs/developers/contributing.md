# Contributing Guide

**Help Improve RivalSearchMCP**

We welcome contributions from the community! This guide explains how to contribute to RivalSearchMCP, whether it's fixing bugs, adding features, or improving documentation.

## How to Contribute

### Types of Contributions
- **Bug fixes** - Fix issues and improve reliability
- **New features** - Add new search engines or tools
- **Documentation** - Improve guides and examples
- **Testing** - Add tests and improve coverage
- **Performance** - Optimize speed and efficiency

### Before You Start
1. **Check existing issues** to see what needs work
2. **Read the [API Reference](api-reference.md)** to understand the codebase
3. **Set up your development environment** using the [Installation Guide](installation.md)

## Development Workflow

### 1. Fork and Clone
```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/RivalSearchMCP.git
cd RivalSearchMCP
```

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 3. Make Changes
- **Follow the coding standards** (see below)
- **Write tests** for new functionality
- **Update documentation** if needed

### 4. Test Your Changes
```bash
# Run the test suite
python -m pytest

# Check code quality
black src/
isort src/
flake8 src/
pylint src/
```

### 5. Commit and Push
```bash
git add .
git commit -m "Add feature: description of your changes"
git push origin feature/your-feature-name
```

### 6. Create a Pull Request
- **Describe your changes** clearly
- **Link related issues** if applicable
- **Include test results** if you added tests

## Coding Standards

### Python Style
- **Follow PEP 8** for code style
- **Use type hints** for function parameters and returns
- **Write docstrings** for all public functions and classes
- **Keep functions focused** and under 50 lines when possible

### Code Quality
- **Use meaningful variable names**
- **Add comments** for complex logic
- **Handle errors gracefully** with proper exception handling
- **Write tests** for new functionality

### Example Code
```python
from typing import List, Optional
from pydantic import BaseModel

class SearchResult(BaseModel):
    """Represents a single search result."""
    
    title: str
    url: str
    snippet: str
    source: str
    
    def get_display_title(self) -> str:
        """Return a formatted title for display."""
        return f"{self.title} - {self.source}"

async def search_web(query: str, num_results: int = 10) -> List[SearchResult]:
    """
    Search the web for the given query.
    
    Args:
        query: The search query string
        num_results: Maximum number of results to return
        
    Returns:
        List of search results
        
    Raises:
        SearchError: If the search fails
    """
    # Implementation here
    pass
```

## Testing

### Writing Tests
- **Test all new functionality**
- **Use descriptive test names**
- **Test both success and failure cases**
- **Mock external dependencies**

### Test Structure
```python
import pytest
from src.core.search import GoogleSearchEngine

class TestGoogleSearchEngine:
    """Test the Google search engine functionality."""
    
    @pytest.fixture
    def search_engine(self):
        """Create a search engine instance for testing."""
        return GoogleSearchEngine()
    
    async def test_search_returns_results(self, search_engine):
        """Test that search returns results for valid queries."""
        results = await search_engine.search("test query")
        assert len(results) > 0
        assert all(hasattr(r, 'title') for r in results)
    
    async def test_search_handles_empty_query(self, search_engine):
        """Test that search handles empty queries gracefully."""
        with pytest.raises(ValueError):
            await search_engine.search("")
```

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_search.py

# Run with coverage
python -m pytest --cov=src

# Run only fast tests
python -m pytest -m "not slow"
```

## Documentation

### Updating Documentation
- **Keep documentation current** with code changes
- **Add examples** for new features
- **Update installation instructions** if needed
- **Check links** work correctly

### Documentation Standards
- **Use clear, simple language**
- **Include code examples**
- **Add screenshots** for UI changes
- **Test all code examples**

## Pull Request Guidelines

### What to Include
- **Clear description** of changes
- **Screenshots** for UI changes
- **Test results** showing everything passes
- **Related issue numbers** if applicable

### Review Process
1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Tests must pass** on all platforms
4. **Documentation updated** if needed

### Common Issues
- **Missing tests** for new functionality
- **Code style violations** (use black/isort)
- **Broken documentation links**
- **Missing type hints**

## Getting Help

### Questions and Discussion
- **GitHub Discussions** for general questions
- **GitHub Issues** for bug reports
- **Pull Request comments** for specific feedback

### Resources
- **API Reference** for code understanding
- **Installation Guide** for setup help
- **Examples** for usage patterns
- **FastMCP Documentation** for framework details

## Recognition

### Contributors
- **All contributors** are listed in the README
- **Significant contributions** get special recognition
- **Regular contributors** may become maintainers

### How to Get Recognition
- **Make quality contributions**
- **Help other contributors**
- **Improve documentation**
- **Report and fix bugs**

## Next Steps

- **Set up your environment** using the [Installation Guide](installation.md)
- **Read the [API Reference](api-reference.md)** to understand the code
- **Find an issue** to work on
- **Join the discussion** in GitHub Discussions

Thank you for contributing to RivalSearchMCP!
