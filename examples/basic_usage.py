"""
Basic usage examples for GridAPI client.

This example demonstrates:
1. Loading configuration from grid_token file
2. Basic CRUD operations (Create, Read, Update, Delete)
3. Querying and filtering
4. Working with nested resources (procedures, subjects, events)
5. CLI command examples

CLI Usage Examples:
- List studies: python -m gridapi.cli studies list
- Get study details: python -m gridapi.cli studies get 100
- List subjects: python -m gridapi.cli studies subjects 100
- List procedures: python -m gridapi.cli studies procedures 100
- List events: python -m gridapi.cli studies events 100
- List event details: python -m gridapi.cli studies event-details 100 10000
- List subject contacts: python -m gridapi.cli studies subject-contacts 100 1000
- JSON output: python -m gridapi.cli studies subjects 100 --format json
- Show help: python -m gridapi.cli --help
"""

import os
from pathlib import Path
from gridapi import GridAPIClient
from gridapi.query import QueryBuilder


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
        print(f"Warning: {config_file} file not found. Using default values.")
        print("Create a grid_token file with:")
        print("grid_token=your-api-token-here")
        print("base_url=https://your-api-url.com")
    
    return config


def main():
    """Demonstrate basic GridAPI usage."""
    
    # Load configuration from grid_token file
    config = load_config_from_file()
    
    # Initialize the client with config file values
    client = GridAPIClient(
        base_url=config.get('base_url', 'https://api.grid.example.com'),
        token=config.get('grid_token')
    )
    
    print("=== GridAPI Basic Usage Examples ===\n")
    
    # Example 1: List studies
    print("1. Listing all studies:")
    studies = client.grid.studies.list()
    for study in studies:
        print(f"  - Study {study.id}: {study.description} (Investigator: {study.investigator})")
    
    # Example 2: Create a new study
    print("\n2. Creating a new study:")
    new_study = client.grid.studies.create({
        "description": "Clinical Trial Study 2024",
        "investigator": "Dr. Jane Smith",
        "status": 1,
        "note": "Phase II clinical trial"
    })
    print(f"  Created study with ID: {new_study.id}")
    
    # Example 3: Get a specific study
    print("\n3. Getting a specific study:")
    study = client.grid.studies.get(new_study.id)
    print(f"  Study: {study.description}")
    print(f"  Investigator: {study.investigator}")
    print(f"  Status: {study.status}")
    
    # Example 4: Update a study
    print("\n4. Updating a study:")
    updated_study = client.grid.studies.update(new_study.id, {
        "description": "Updated Clinical Trial Study 2024",
        "status": 2
    })
    print(f"  Updated study: {updated_study.description}")
    
    # Example 5: Search studies
    print("\n5. Searching studies:")
    search_results = client.grid.studies.search("clinical")
    print(f"  Found {len(search_results)} studies matching 'clinical'")
    
    # Example 6: Filter studies
    print("\n6. Filtering studies by investigator:")
    filtered_studies = client.grid.studies.filter(investigator="Dr. Jane Smith")
    print(f"  Found {len(filtered_studies)} studies by Dr. Jane Smith")
    
    # Example 7: Complex query with QueryBuilder
    print("\n7. Complex query with QueryBuilder:")
    query = QueryBuilder()
    query.search("trial").filter_gt("status", 0).order_by("created_at", ascending=False)
    complex_results = client.grid.studies.list(query=query)
    print(f"  Found {len(complex_results)} studies with complex query")
    
    # Example 8: Working with nested resources
    print("\n8. Working with nested resources:")
    study_id = new_study.id
    
    # Get study events
    events = client.grid.study(study_id).events.list()
    print(f"  Study {study_id} has {len(events)} events")
    
    # Get study subjects
    subjects = client.grid.study(study_id).subjects.list()
    print(f"  Study {study_id} has {len(subjects)} subjects")
    
    # Example 9: Image API usage
    print("\n9. Image API usage:")
    acquisitions = client.image.acquisitions.list()
    print(f"  Found {len(acquisitions)} acquisitions")
    
    actions = client.image.actions.list(status="completed")
    print(f"  Found {len(actions)} completed actions")
    
    # Example 10: CLI Usage Examples
    print("\n10. CLI Usage Examples:")
    print("  You can also use the GridAPI CLI for quick access:")
    print("  - List studies: python -m gridapi.cli studies list")
    print("  - Get study details: python -m gridapi.cli studies get 100")
    print("  - List subjects: python -m gridapi.cli studies subjects 100")
    print("  - List procedures: python -m gridapi.cli studies procedures 100")
    print("  - List events: python -m gridapi.cli studies events 100")
    print("  - List event details: python -m gridapi.cli studies event-details 100 10000")
    print("  - List subject contacts: python -m gridapi.cli studies subject-contacts 100 1000")
    print("  - JSON output: python -m gridapi.cli studies subjects 100 --format json")
    print("  - Show help: python -m gridapi.cli --help")
    
    # Example 11: Error handling
    print("\n11. Error handling:")
    try:
        non_existent_study = client.grid.studies.get(99999)
    except Exception as e:
        print(f"  Expected error for non-existent study: {type(e).__name__}")
    
    print("\n=== Examples completed ===")


if __name__ == "__main__":
    main()
