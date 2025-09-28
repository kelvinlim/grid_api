"""
Simple example showing how to use GridAPI with grid_token file.

This example demonstrates:
1. Loading configuration from grid_token file
2. Basic API client usage
3. CLI command examples

CLI Usage Examples:
- List studies: python -m gridapi.cli studies list
- Get study details: python -m gridapi.cli studies get 100
- List subjects: python -m gridapi.cli studies subjects 100
- List procedures: python -m gridapi.cli studies procedures 100
- List events: python -m gridapi.cli studies events 100
- JSON output: python -m gridapi.cli studies subjects 100 --format json
- Show help: python -m gridapi.cli --help
"""

from pathlib import Path
from gridapi import GridAPIClient


def load_config_from_file(config_file="grid_token"):
    """Load configuration from grid_token file."""
    config_path = Path(config_file)
    config = {}
    
    if config_path.exists():
        with open(config_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    else:
        print(f"Warning: {config_file} file not found.")
        print("Create a grid_token file with:")
        print("grid_token=your-api-token-here")
        print("base_url=https://your-api-url.com")
        return None
    
    return config


def main():
    """Simple example using grid_token file."""
    
    # Load configuration from grid_token file
    config = load_config_from_file()
    
    if not config:
        return
    
    # Initialize the client
    client = GridAPIClient(
        base_url=config.get('base_url', 'https://api.grid.example.com'),
        token=config.get('grid_token')
    )
    
    print("=== Simple GridAPI Example ===\n")
    
    try:
        # List studies
        print("Fetching studies...")
        studies = client.grid.studies.list()
        print(f"Found {len(studies)} studies")
        
        # Show first few studies
        for i, study in enumerate(studies[:3]):
            print(f"  {i+1}. {study.description} (ID: {study.id})")
        
        if len(studies) > 3:
            print(f"  ... and {len(studies) - 3} more")
            
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure your grid_token file has valid credentials.")


if __name__ == "__main__":
    main()
