# GridAPI Python Package - Installation Guide

## Quick Start

### 1. Install the Package

```bash
# Install from source (core dependencies only)
pip install -e .

# Or install with optional dependencies (use quotes for shell compatibility)
pip install -e ".[async,cli,dev]"
```

**Important Notes**:
- Don't run `pip install cli` - that's not a valid command
- The `cli` is an optional dependency group for our GridAPI package
- Use quotes around `.[cli]` to prevent shell interpretation issues

### 2. Basic Usage

```python
from gridapi import GridAPIClient

# Initialize client
client = GridAPIClient(
    base_url="https://your-grid-api.com",
    token="your-api-token"
)

# List studies
studies = client.grid.studies.list()
print(f"Found {len(studies)} studies")

# Create a new study
study = client.grid.studies.create({
    "description": "My Research Study",
    "investigator": "Dr. Smith",
    "status": 1
})
print(f"Created study {study.id}")
```

## Development Setup

### 1. Clone and Setup

```bash
git clone <repository-url>
cd grid_api
pip install -e .[dev]
```

### 2. Run Tests

```bash
pytest tests/
```

### 3. Run Examples

```bash
# Basic usage
python examples/basic_usage.py

# Advanced usage
python examples/advanced_usage.py
```

### 4. Use CLI Tool

The CLI automatically reads configuration from a `grid_token` file in the current directory.

**Create a configuration file:**
```bash
# Create grid_token file
echo "grid_token=your-api-token-here" > grid_token
echo "base_url=https://your-api-url.com" >> grid_token
```

**Use the CLI:**
```bash
# List studies (reads from grid_token file)
gridapi studies list

# Get specific study
gridapi studies get 123

# Create study
gridapi studies create --description "Test Study" --investigator "Dr. Test"

# Show current configuration
gridapi config

# Override config file values
gridapi --base-url https://other-api.com studies list
```

## Configuration

### Environment Variables

You can set default values using environment variables:

```bash
export GRIDAPI_BASE_URL="https://your-grid-api.com"
export GRIDAPI_TOKEN="your-api-token"
```

Then use the client without explicit configuration:

```python
from gridapi import GridAPIClient

client = GridAPIClient()  # Uses environment variables
```

### Authentication Methods

#### Token Authentication
```python
client = GridAPIClient(
    base_url="https://api.example.com",
    token="your-api-token"
)
```

#### Session Authentication
```python
client = GridAPIClient(
    base_url="https://api.example.com",
    session_id="your-session-id"
)
```

## Package Structure

```
gridapi/
├── __init__.py              # Main package exports
├── client.py                # Main client classes
├── auth.py                  # Authentication handling
├── exceptions.py            # Custom exceptions
├── models/                  # Pydantic data models
│   ├── base.py             # Base model classes
│   ├── grid.py             # Grid API models
│   └── image.py            # Image API models
├── managers/                # Resource managers
│   ├── base.py             # Base manager class
│   ├── grid_manager.py     # Grid API managers
│   ├── image_manager.py    # Image API managers
│   └── taskflow_manager.py # Taskflow API managers
├── query/                   # Query building
│   ├── builder.py          # Query builder
│   └── filters.py          # Filter utilities
├── utils/                   # Utility functions
│   ├── validators.py       # Data validation
│   └── helpers.py          # Helper functions
└── cli.py                  # Command-line interface
```

## Features

- ✅ **Type-safe** interactions with all Grid API endpoints
- ✅ **Intuitive** resource management with proper abstractions
- ✅ **Comprehensive** CRUD operations for all data models
- ✅ **Advanced** querying and filtering capabilities
- ✅ **Robust** authentication handling
- ✅ **Excellent** developer experience with proper error handling
- ✅ **CLI tools** for command-line usage
- ✅ **Comprehensive** documentation and examples
- ✅ **Unit tests** for reliability

## Next Steps

1. **Configure your API endpoint** and authentication
2. **Explore the examples** in the `examples/` directory
3. **Read the API documentation** for your specific Grid API instance
4. **Start building** your application with the GridAPI client!

## Support

For questions, issues, or contributions, please refer to the project repository or contact the development team.
