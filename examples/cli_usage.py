"""
CLI Usage Examples for GridAPI.

This example demonstrates how to use the GridAPI command-line interface
for common tasks and data exploration.

Prerequisites:
1. Create a 'grid_token' file in your project directory with:
   grid_token=your-api-token-here
   base_url=https://your-api-url.com

2. Install the CLI dependencies:
   pip install -e ".[cli]"

CLI Commands Overview:
- studies: Manage studies and related resources
  - list: List all studies
  - get: Get a specific study
  - create: Create a new study
  - procedures: List procedures for a study
  - subjects: List subjects for a study
  - events: List events for a study
  - event-details: List details for a specific event
  - subject-contacts: List contact info for a subject

- actions: Manage image actions
  - list: List all actions

All list commands support --format json for JSON output.
"""

import subprocess
import sys
from pathlib import Path


def run_cli_command(command):
    """Run a CLI command and return the output."""
    try:
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e}")
        print(f"Error output: {e.stderr}")
        return None


def main():
    """Demonstrate CLI usage examples."""
    
    print("=== GridAPI CLI Usage Examples ===\n")
    
    # Check if grid_token file exists
    if not Path("grid_token").exists():
        print("❌ grid_token file not found!")
        print("Create a grid_token file with:")
        print("grid_token=your-api-token-here")
        print("base_url=https://your-api-url.com")
        return
    
    print("✅ grid_token file found\n")
    
    # Example 1: Show help
    print("1. Show CLI help:")
    print("   Command: python -m gridapi.cli --help")
    help_output = run_cli_command("python -m gridapi.cli --help")
    if help_output:
        print("   Help output:")
        for line in help_output.split('\n')[:10]:  # Show first 10 lines
            print(f"   {line}")
        print("   ...")
    
    # Example 2: List studies
    print("\n2. List studies:")
    print("   Command: python -m gridapi.cli studies list")
    studies_output = run_cli_command("python -m gridapi.cli studies list")
    if studies_output:
        print("   Studies found:")
        for line in studies_output.split('\n')[:5]:  # Show first 5 lines
            print(f"   {line}")
        print("   ...")
    
    # Example 3: Get study details
    print("\n3. Get study details:")
    print("   Command: python -m gridapi.cli studies get 100")
    study_output = run_cli_command("python -m gridapi.cli studies get 100")
    if study_output:
        print("   Study details:")
        for line in study_output.split('\n')[:8]:  # Show first 8 lines
            print(f"   {line}")
        print("   ...")
    
    # Example 4: List subjects
    print("\n4. List subjects for study 100:")
    print("   Command: python -m gridapi.cli studies subjects 100")
    subjects_output = run_cli_command("python -m gridapi.cli studies subjects 100")
    if subjects_output:
        print("   Subjects found:")
        for line in subjects_output.split('\n')[:5]:  # Show first 5 lines
            print(f"   {line}")
        print("   ...")
    
    # Example 5: List procedures
    print("\n5. List procedures for study 100:")
    print("   Command: python -m gridapi.cli studies procedures 100")
    procedures_output = run_cli_command("python -m gridapi.cli studies procedures 100")
    if procedures_output:
        print("   Procedures found:")
        for line in procedures_output.split('\n')[:5]:  # Show first 5 lines
            print(f"   {line}")
        print("   ...")
    
    # Example 6: List events
    print("\n6. List events for study 100:")
    print("   Command: python -m gridapi.cli studies events 100")
    events_output = run_cli_command("python -m gridapi.cli studies events 100")
    if events_output:
        print("   Events found:")
        for line in events_output.split('\n')[:5]:  # Show first 5 lines
            print(f"   {line}")
        print("   ...")
    
    # Example 7: JSON output
    print("\n7. Get subjects as JSON:")
    print("   Command: python -m gridapi.cli studies subjects 100 --format json")
    json_output = run_cli_command("python -m gridapi.cli studies subjects 100 --format json")
    if json_output:
        print("   JSON output (first 500 characters):")
        print(f"   {json_output[:500]}...")
    
    # Example 8: Show configuration
    print("\n8. Show current configuration:")
    print("   Command: python -m gridapi.cli config")
    config_output = run_cli_command("python -m gridapi.cli config")
    if config_output:
        print("   Configuration:")
        for line in config_output.split('\n'):
            print(f"   {line}")
    
    print("\n=== CLI Examples completed ===")
    print("\nFor more information, run:")
    print("python -m gridapi.cli --help")


if __name__ == "__main__":
    main()
