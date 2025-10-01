# LNPI GridAPI Python Client

A comprehensive Python client library for interacting with the LNPI Grid API, providing type-safe, intuitive access to research studies, medical imaging data, and workflow management.

## Features

- 🚀 **Type-safe** interactions with all Grid API endpoints
- 🏗️ **Intuitive** resource management with proper abstractions
- 📊 **Comprehensive** CRUD operations for all data models
- 🔍 **Advanced** querying and filtering capabilities
- 🔐 **Robust** authentication handling
- ⚡ **Async support** for high-performance applications
- 📚 **Excellent** developer experience with proper error handling

## Installation

### From PyPI
```bash
pip install lnpi_gridapi
```

### From Source
```bash
git clone https://github.com/kelvinlim/gridapi.git
cd gridapi
pip install -e .
```

### With Optional Dependencies
```bash
# For CLI functionality
pip install lnpi_gridapi[cli]

# For async support
pip install lnpi_gridapi[async]

# For development
pip install lnpi_gridapi[dev]

# All features
pip install lnpi_gridapi[all]
```

### Windows Standalone Executable
For users who don't want to install Python:

1. **Download**: Get the pre-built executable from releases
   - **Windows**: `gridapi-windows.exe`
   - **macOS**: `gridapi-macos`
   - **Linux**: `gridapi-linux`
2. **Configure**: Create a `grid_token` file with your API credentials
3. **Run**: Execute the executable directly from command line

See [WINDOWS_BUILD.md](WINDOWS_BUILD.md) for detailed instructions on building cross-platform executables.
See [DEPLOYMENT.md](DEPLOYMENT.md) for information about automated releases and deployment.

## Releases

### Latest Release
Download the latest release from [GitHub Releases](https://github.com/kelvinlim/grid_api/releases):

- **Windows**: `gridapi-windows.exe`
- **macOS**: `gridapi-macos`  
- **Linux**: `gridapi-linux`

### Release Process
Releases are automatically created when version tags are pushed:

```bash
git tag v1.0.0
git push origin v1.0.0
```

This triggers GitHub Actions to:
1. Build executables for all platforms
2. Create a GitHub release with downloadable assets
3. Generate checksums for verification

## Quick Start

### Using grid_token file (Recommended)

Create a `grid_token` file in your project directory:
```
grid_token=your-api-token-here
base_url=https://api.grid.example.com
```

Then use it in your code:
```python
from pathlib import Path
from gridapi import GridAPIClient

# Load config from grid_token file
config_path = Path("grid_token")
config = {}
if config_path.exists():
    with open(config_path, 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                config[key] = value

# Initialize client
client = GridAPIClient(
    base_url=config.get('base_url', 'https://api.grid.example.com'),
    token=config.get('grid_token')
)

# Create a study
study = client.grid.studies.create({
    "description": "Clinical Trial Study",
    "investigator": "Dr. Jane Smith",
    "status": 1
})

# List studies with filtering
studies = client.grid.studies.list(
    investigator="Dr. Smith",
    status=1
)

# Access nested resources
events = client.grid.studies(study.id).events.list()
```

## API Categories

### Grid API
- **Studies**: Research study management
- **Datatypes**: Data type definitions
- **Subjects**: Study participants
- **Events**: Study events and details
- **Procedures**: Study procedures

### Image API
- **Acquisitions**: Image acquisition data
- **Actions**: Image processing actions
- **Scanner Types**: Scanner configurations
- **Raw Data**: Raw image data management

### Taskflow API
- **Measures**: Study measures
- **Participants**: Workflow participants

## Advanced Usage

### Complex Filtering
```python
# Advanced querying
studies = client.grid.studies.list(
    search="clinical trial",
    ordering="-created_at",
    status__gte=1
)

# Nested resource operations
subject = client.grid.studies(123).subjects(456).get()
contacts = client.grid.studies(123).subjects(456).contacts.list()
```

### Async Support
```python
import asyncio
from gridapi import AsyncGridAPIClient

async def main():
    client = AsyncGridAPIClient(
        base_url="https://api.grid.example.com",
        token="your-api-token"
    )
    
    studies = await client.grid.studies.list()
    return studies

# Run async code
studies = asyncio.run(main())
```

## Examples

Check out the examples directory for comprehensive usage examples:

- `examples/simple_example.py` - Basic usage with grid_token file
- `examples/basic_usage.py` - Common operations and patterns
- `examples/advanced_usage.py` - Complex queries and advanced features
- `examples/cli_usage.py` - Command-line interface examples
- `examples/event_details_example.py` - Event details functionality examples

All examples use the `grid_token` file for configuration, making them easy to run.

## CLI Usage

The CLI automatically reads configuration from a `grid_token` file and provides comprehensive access to all GridAPI resources:

```bash
# Create configuration file
echo "grid_token=your-api-token-here" > grid_token
echo "base_url=https://your-api-url.com" >> grid_token

# Study management
gridapi studies list                                    # List all studies
gridapi studies get 100                               # Get study details
gridapi studies create --description "Test Study" --investigator "Dr. Test"

# Study resources
gridapi studies subjects 100                          # List subjects for study 100
gridapi studies procedures 100                         # List procedures for study 100
gridapi studies events 100                            # List events for study 100
gridapi studies event-details 100 10000               # List details for event 10000
gridapi studies subject-contacts 100 1000             # List contacts for subject 1000

# Image management
gridapi actions list                                   # List all image actions
gridapi actions list --status completed               # List completed actions

# Output formats
gridapi studies subjects 100 --format json            # JSON output
gridapi studies subjects 100 --format table           # Table output (default)

# Configuration
gridapi config                                         # Show current configuration
gridapi --help                                         # Show help
```

### CLI Features

- **Automatic Configuration**: Reads from `grid_token` file by default
- **Multiple Output Formats**: Table (default) and JSON output
- **Comprehensive Coverage**: Access to all study resources and nested data
- **Command Overrides**: Override config file with command-line options
- **Rich Output**: Beautiful tables with colors and formatting
- **Error Handling**: Clear error messages and validation

## Authentication

The GridAPI client supports multiple authentication methods:

```python
# Token authentication
client = GridAPIClient(
    base_url="https://api.grid.example.com",
    token="your-api-token"
)

# Cookie authentication
client = GridAPIClient(
    base_url="https://api.grid.example.com",
    session_id="your-session-id"
)
```

## Error Handling

```python
from gridapi.exceptions import GridAPIError, ValidationError

try:
    study = client.grid.studies.create(invalid_data)
except ValidationError as e:
    print(f"Validation error: {e}")
except GridAPIError as e:
    print(f"API error: {e}")
```

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests to our GitHub repository.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
