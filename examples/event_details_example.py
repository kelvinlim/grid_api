#!/usr/bin/env python3
"""
Example demonstrating how to retrieve event details using GridAPI.

This example shows both high-level API usage and CLI usage for getting
event details for a specific event in a study.
"""

import sys
from pathlib import Path

# Add the parent directory to the path so we can import gridapi
sys.path.insert(0, str(Path(__file__).parent.parent))

from gridapi import GridAPIClient
from gridapi.exceptions import GridAPIError
from gridapi.managers.grid_manager import StudyContextManager


def load_config_from_file(config_file="grid_token"):
    """Load configuration from a file."""
    config = {}
    config_path = Path(config_file)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file '{config_file}' not found")
    
    with open(config_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    
    return config


def main():
    """Demonstrate event details functionality."""
    print("=== GridAPI Event Details Example ===\n")
    
    try:
        # Load configuration
        config = load_config_from_file()
        token = config.get('grid_token')
        base_url = config.get('base_url')
        
        if not token or not base_url:
            print("Error: Missing 'grid_token' or 'base_url' in configuration file")
            return
        
        # Initialize client
        client = GridAPIClient(token=token, base_url=base_url)
        print(f"✅ Connected to: {base_url}")
        
        # Example: Get event details for event 56320 in study 316
        study_id = 316
        event_id = 56320
        
        print(f"\n📋 Getting event details for Event {event_id} in Study {study_id}")
        
        # Method 1: Using raw client request (recommended for event details)
        print("\n🔧 Method 1: Raw API request (recommended)")
        try:
            details_data = client.request("GET", f"/api/grid/studies/{study_id}/events/{event_id}/details/")
            
            print(f"Found {len(details_data)} event details:")
            for detail in details_data:
                print(f"  - ID: {detail.get('id')}")
                print(f"    Description: {detail.get('description', 'N/A')}")
                print(f"    Data Type ID: {detail.get('datatype_id')}")
                print(f"    JSON Data: {detail.get('json_data')}")
                print(f"    Prior Detail ID: {detail.get('prior_detail_id')}")
                print()
                
        except GridAPIError as e:
            print(f"❌ Raw API error: {e}")
        
        # Method 2: High-level API (has validation issues with nested resources)
        print("\n🔧 Method 2: High-level API (note: has validation issues)")
        print("   The high-level API has Pydantic validation issues with nested resources")
        print("   because the API doesn't return all required fields (like study_id)")
        print("   For event details, use the raw API approach above.")
        
        print("\n💡 CLI Usage:")
        print(f"   gridapi studies event-details {study_id} {event_id}")
        print(f"   gridapi studies event-details {study_id} {event_id} --format json")
        
    except FileNotFoundError as e:
        print(f"❌ Configuration error: {e}")
        print("Please create a 'grid_token' file with your API credentials:")
        print("  grid_token=your-api-token-here")
        print("  base_url=https://your-api-url.com")
    except GridAPIError as e:
        print(f"❌ API error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
