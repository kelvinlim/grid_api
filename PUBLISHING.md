# Publishing Guide for GridAPI

This guide explains how to build and publish the GridAPI Python package to PyPI.

## Prerequisites

1. **Install build tools:**
   ```bash
   pip install build twine
   ```

2. **Create PyPI accounts:**
   - [PyPI](https://pypi.org/account/register/) - Production package index
   - [Test PyPI](https://test.pypi.org/account/register/) - Testing package index

3. **Configure credentials:**
   ```bash
   # Create ~/.pypirc file
   [distutils]
   index-servers = pypi testpypi
   
   [pypi]
   username = __token__
   password = pypi-your-api-token-here
   
   [testpypi]
   repository = https://test.pypi.org/legacy/
   username = __token__
   password = pypi-your-test-api-token-here
   ```

## Quick Start

Use the provided build script for easy publishing:

```bash
# Clean build artifacts
python build.py --clean

# Build package only
python build.py --build

# Test package installation
python build.py --test

# Publish to Test PyPI
python build.py --test-pypi

# Publish to PyPI (production)
python build.py --publish
```

## Manual Publishing Steps

### 1. Clean Build Artifacts

```bash
# Remove old build artifacts
rm -rf build/ dist/ *.egg-info/
find . -type d -name __pycache__ -exec rm -rf {} +
```

### 2. Build Package

```bash
# Build source distribution and wheel
python -m build

# Verify the built package
twine check dist/*
```

### 3. Test Package

```bash
# Test installation in a clean environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate
pip install dist/*.whl
python -c "import gridapi; print('Success!')"
deactivate
rm -rf test_env
```

### 4. Publish to Test PyPI

```bash
# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ gridapi
```

### 5. Publish to PyPI

```bash
# Upload to PyPI (production)
twine upload dist/*
```

## Package Structure

The package uses modern Python packaging with `pyproject.toml`:

```
gridapi/
├── pyproject.toml          # Package configuration
├── MANIFEST.in            # Files to include in package
├── LICENSE                # MIT License
├── README.md              # Package documentation
├── CHANGELOG.md           # Version history
├── INSTALLATION.md        # Installation guide
├── build.py               # Build and publish script
└── gridapi/               # Package source code
    ├── __init__.py
    ├── client.py
    ├── auth.py
    ├── exceptions.py
    ├── cli.py
    ├── py.typed           # Type hints marker
    ├── models/            # Data models
    ├── managers/          # Resource managers
    ├── query/             # Query builders
    └── utils/             # Utilities
```

## Version Management

### Updating Version

1. **Update version in `pyproject.toml`:**
   ```toml
   [project]
   version = "1.0.1"  # Update version number
   ```

2. **Update `CHANGELOG.md`** with new changes

3. **Commit and tag:**
   ```bash
   git add .
   git commit -m "Release version 1.0.1"
   git tag v1.0.1
   git push origin main --tags
   ```

### Semantic Versioning

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.1.0): New features, backward compatible
- **PATCH** (0.0.1): Bug fixes, backward compatible

## Quality Checks

Before publishing, ensure:

1. **Code Quality:**
   ```bash
   # Format code
   black gridapi/ tests/ examples/
   isort gridapi/ tests/ examples/
   
   # Type checking
   mypy gridapi/
   
   # Linting
   flake8 gridapi/
   ```

2. **Tests Pass:**
   ```bash
   pytest tests/ -v
   ```

3. **Documentation:**
   - README.md is up to date
   - All docstrings are complete
   - Examples work correctly

## Troubleshooting

### Common Issues

1. **"Package already exists" error:**
   - Update version number in `pyproject.toml`
   - Delete old build artifacts and rebuild

2. **Authentication errors:**
   - Check `~/.pypirc` configuration
   - Verify API tokens are correct
   - Use `twine upload --repository testpypi dist/*` for Test PyPI

3. **Build errors:**
   - Ensure all dependencies are installed
   - Check `pyproject.toml` syntax
   - Verify all required files exist

### Getting Help

- Check [PyPI documentation](https://packaging.python.org/)
- Review [setuptools documentation](https://setuptools.pypa.io/)
- Check package logs for detailed error messages

## Post-Publication

After successful publication:

1. **Verify installation:**
   ```bash
   pip install gridapi
   python -c "import gridapi; print(gridapi.__version__)"
   ```

2. **Update documentation** if needed

3. **Announce release** to users

4. **Monitor for issues** and respond to user feedback

## Security Notes

- Never commit API tokens or passwords
- Use environment variables for sensitive data
- Regularly rotate API tokens
- Keep dependencies updated for security patches
