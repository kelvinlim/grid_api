"""
Advanced usage examples for GridAPI client.

This example demonstrates:
1. Loading configuration from grid_token file
2. Advanced querying and filtering
3. Complex data manipulation
4. Error handling and validation
5. Working with nested resources
6. CLI command examples

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

from datetime import datetime, date
from pathlib import Path
from gridapi import GridAPIClient
from gridapi.query import QueryBuilder, FilterBuilder, Ordering
from gridapi.models.grid import Study
from gridapi.exceptions import ValidationError, NotFoundError


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
    """Demonstrate advanced GridAPI usage."""
    
    # Load configuration from grid_token file
    config = load_config_from_file()
    
    # Initialize the client with config file values
    client = GridAPIClient(
        base_url=config.get('base_url', 'https://api.grid.example.com'),
        token=config.get('grid_token')
    )
    
    print("=== GridAPI Advanced Usage Examples ===\n")
    
    # Example 1: Pagination
    print("1. Pagination example:")
    query = QueryBuilder().paginate(page=1, page_size=10)
    paginated_results = client.grid.studies.list(query=query)
    
    if isinstance(paginated_results, dict):
        print(f"  Total studies: {paginated_results['count']}")
        print(f"  Current page: {len(paginated_results['results'])} studies")
        print(f"  Has next page: {paginated_results['next'] is not None}")
    else:
        print(f"  Retrieved {len(paginated_results)} studies")
    
    # Example 2: Complex filtering
    print("\n2. Complex filtering:")
    filter_builder = FilterBuilder()
    filter_builder.contains("description", "clinical").gte("status", 1).is_not_null("investigator")
    filters = filter_builder.build()
    
    filtered_studies = client.grid.studies.list(**filters)
    print(f"  Found {len(filtered_studies)} studies with complex filters")
    
    # Example 3: Multiple ordering
    print("\n3. Multiple ordering:")
    orderings = [
        Ordering("status", ascending=False),
        Ordering("created_at", ascending=True)
    ]
    query = QueryBuilder().order_by_multiple(orderings)
    ordered_studies = client.grid.studies.list(query=query)
    print(f"  Retrieved {len(ordered_studies)} studies with multiple ordering")
    
    # Example 4: Working with Pydantic models
    print("\n4. Working with Pydantic models:")
    
    # Create study using model
    study_data = Study(
        description="Model-based Study",
        investigator="Dr. Model User",
        status=1,
        start_date=date.today()
    )
    
    print(f"  Created study model: {study_data.description}")
    print(f"  Model validation: {study_data.model_validate(study_data.dict())}")
    
    # Convert to dict for API
    study_dict = study_data.to_dict()
    print(f"  Model as dict: {study_dict}")
    
    # Example 5: Batch operations
    print("\n5. Batch operations:")
    studies_to_create = [
        {"description": f"Batch Study {i}", "investigator": f"Dr. Batch {i}", "status": 1}
        for i in range(1, 4)
    ]
    
    created_studies = []
    for study_data in studies_to_create:
        try:
            study = client.grid.studies.create(study_data)
            created_studies.append(study)
            print(f"  Created study {study.id}: {study.description}")
        except Exception as e:
            print(f"  Failed to create study: {e}")
    
    # Example 6: Nested resource management
    print("\n6. Nested resource management:")
    if created_studies:
        study = created_studies[0]
        study_id = study.id
        
        # Create study event
        event_data = {
            "name": "Baseline Visit",
            "description": "Initial study visit",
            "event_date": date.today()
        }
        
        try:
            event = client.grid.study(study_id).events.create(event_data)
            print(f"  Created event {event.id} for study {study_id}")
            
            # Create event detail
            detail_data = {
                "name": "Blood Pressure",
                "description": "Systolic and diastolic measurements",
                "value": "120/80"
            }
            
            detail = client.grid.study(study_id).event(event.id).details.create(detail_data)
            print(f"  Created detail {detail.id} for event {event.id}")
            
        except Exception as e:
            print(f"  Error creating nested resources: {e}")
    
    # Example 7: Data validation
    print("\n7. Data validation:")
    try:
        # This should fail validation
        invalid_study = Study(
            description="",  # Empty description
            investigator="Dr. Test",
            status=-1  # Invalid status
        )
    except ValidationError as e:
        print(f"  Validation error caught: {e}")
    
    # Example 8: Error handling patterns
    print("\n8. Error handling patterns:")
    
    def safe_get_study(client, study_id):
        """Safely get a study with proper error handling."""
        try:
            return client.grid.studies.get(study_id)
        except NotFoundError:
            print(f"  Study {study_id} not found")
            return None
        except ValidationError as e:
            print(f"  Validation error for study {study_id}: {e}")
            return None
        except Exception as e:
            print(f"  Unexpected error for study {study_id}: {e}")
            return None
    
    # Test with non-existent study
    safe_get_study(client, 99999)
    
    # Example 9: Query building patterns
    print("\n9. Query building patterns:")
    
    def build_study_query(investigator=None, status_min=None, date_from=None, date_to=None):
        """Build a complex study query."""
        query = QueryBuilder()
        
        if investigator:
            query.filter_contains("investigator", investigator)
        
        if status_min is not None:
            query.filter_gte("status", status_min)
        
        if date_from:
            query.filter_gte("start_date", date_from)
        
        if date_to:
            query.filter_lte("end_date", date_to)
        
        query.order_by("created_at", ascending=False)
        return query
    
    # Use the query builder
    complex_query = build_study_query(
        investigator="Dr. Smith",
        status_min=1,
        date_from=date(2024, 1, 1)
    )
    
    results = client.grid.studies.list(query=complex_query)
    print(f"  Complex query returned {len(results)} studies")
    
    # Example 10: Performance optimization
    print("\n10. Performance optimization:")
    
    # Use specific fields only (if API supports it)
    query = QueryBuilder().page_size(50)  # Larger page size for fewer requests
    
    start_time = datetime.now()
    studies = client.grid.studies.list(query=query)
    end_time = datetime.now()
    
    print(f"  Retrieved {len(studies)} studies in {(end_time - start_time).total_seconds():.2f} seconds")
    
    print("\n=== Advanced examples completed ===")


if __name__ == "__main__":
    main()
