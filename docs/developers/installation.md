# Developer Installation

**Set Up Your Development Environment**

This guide covers the complete setup process for developers who want to run RivalSearchMCP locally, contribute to the codebase, or customize the server.

## Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **Git**: Latest version
- **Memory**: At least 2GB RAM
- **Storage**: 1GB free space

### Python Version Check
```bash
python3 --version
# Should show Python 3.8.0 or higher
```

## Step 1: Clone the Repository

```bash
git clone https://github.com/damionrashford/RivalSearchMCP.git
cd RivalSearchMCP
```

## Step 2: Set Up Virtual Environment

### Create Virtual Environment
```bash
# On macOS/Linux
python3 -m venv .venv

# On Windows
python -m venv .venv
```

### Activate Virtual Environment
```bash
# On macOS/Linux
source .venv/bin/activate

# On Windows
.venv\Scripts\activate
```

## Step 3: Install Dependencies

### Install from Requirements
```bash
pip install -r requirements.txt
```

### Install Development Dependencies
```bash
pip install -r requirements-dev.txt  # If available
pip install black isort flake8 pylint  # Code quality tools
```

## Step 4: Verify Installation

### Check Python Path
```bash
which python
# Should point to your virtual environment
```

### Test Import
```bash
python -c "import src.server; print('Import successful!')"
```

## Step 5: Run the Development Server

### Start Server
```bash
python -m src.server
```

### Test with MCP Client
```bash
# In another terminal, test the connection
python test_server.py
```

## Configuration

### Environment Variables
```bash
export RIVAL_SEARCH_DEBUG=true
export RIVAL_SEARCH_LOG_LEVEL=DEBUG
export RIVAL_SEARCH_MAX_WORKERS=4
```

### Configuration File
Create `config/local.py` for local development:
```python
DEBUG = True
LOG_LEVEL = "DEBUG"
MAX_WORKERS = 4
SEARCH_TIMEOUT = 30
```

## Development Tools

### Code Quality
```bash
# Format code
black src/
isort src/

# Lint code
flake8 src/
pylint src/
```

### Testing
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_search.py

# Run with coverage
python -m pytest --cov=src
```

### Type Checking
```bash
# Check types
mypy src/

# Install mypy if needed
pip install mypy
```

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Check Python path
which python
```

#### Dependency Issues
```bash
# Upgrade pip
pip install --upgrade pip

# Clear cache and reinstall
pip cache purge
pip install -r requirements.txt
```

#### Permission Issues
```bash
# On macOS/Linux, you might need
chmod +x scripts/*.sh
```

### Debug Mode
```bash
# Enable debug logging
export RIVAL_SEARCH_DEBUG=true
python -m src.server --debug
```

## Next Steps

- [API Reference](api-reference.md) - Understand the codebase
- [Contributing Guide](contributing.md) - Start contributing


## Getting Help

- **Issues**: [GitHub Issues](https://github.com/damionrashford/RivalSearchMCP/issues)
- **Discussions**: [GitHub Discussions](https://github.com/damionrashford/RivalSearchMCP/discussions)
- **Documentation**: Check other developer guides
