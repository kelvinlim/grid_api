"""
Command-line interface for GridAPI.
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import click
from click import HelpFormatter
from rich.console import Console
from rich.table import Table
from rich.json import JSON

from gridapi.client import GridAPIClient
from gridapi.exceptions import GridAPIError

# Get version from package metadata
try:
    # First try to read from pyproject.toml for development
    import re
    with open('pyproject.toml', 'r') as f:
        content = f.read()
        match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            __version__ = match.group(1)
        else:
            raise ValueError("Version not found in pyproject.toml")
except Exception:
    # Fallback to package metadata
    try:
        from importlib.metadata import version
        __version__ = version('gridapi')
    except ImportError:
        # Fallback for older Python versions
        try:
            from importlib_metadata import version
            __version__ = version('gridapi')
        except ImportError:
            __version__ = 'unknown'
    except Exception:
        __version__ = 'dev'

console = Console()


def load_config_file(config_file: Optional[str] = None) -> Dict[str, str]:
    """
    Load configuration from file.
    
    Args:
        config_file: Path to config file. If None, uses 'grid_token' in current directory.
        
    Returns:
        Dictionary of configuration values
    """
    if config_file is None:
        config_file = "grid_token"
    
    config_path = Path(config_file)
    config = {}
    
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
        except Exception as e:
            console.print(f"[yellow]Warning: Could not read config file {config_file}: {e}[/yellow]")
    
    return config


def get_client_from_context(ctx) -> GridAPIClient:
    """
    Create GridAPIClient from context and config file.
    
    Args:
        ctx: Click context
        
    Returns:
        Configured GridAPIClient instance
    """
    # Load config from file
    config_file = ctx.obj.get('config_file')
    config = load_config_file(config_file)
    
    # Get values from context (command line) or config file
    base_url = ctx.obj.get('base_url') or config.get('base_url', 'https://api.grid.example.com')
    token = ctx.obj.get('token') or config.get('grid_token')
    session_id = ctx.obj.get('session_id') or config.get('session_id')
    
    if not token and not session_id:
        console.print("[red]Error: No authentication provided. Use --token, --session-id, or create a 'grid_token' file.[/red]")
        console.print("[yellow]Example grid_token file content:[/yellow]")
        console.print("[yellow]grid_token=your-api-token-here[/yellow]")
        console.print("[yellow]base_url=https://your-api-url.com[/yellow]")
        sys.exit(1)
    
    return GridAPIClient(
        base_url=base_url,
        token=token,
        session_id=session_id
    )


@click.group(context_settings={
    'help_option_names': ['-h', '--help'],
    'max_content_width': 100,
    'terminal_width': 120
}, help=f"GridAPI command-line interface (version {__version__})")
@click.option('--base-url', help='Base URL for Grid API (overrides config file)')
@click.option('--token', help='API token for authentication (overrides config file)')
@click.option('--session-id', help='Session ID for cookie authentication (overrides config file)')
@click.option('--config-file', help='Path to configuration file (default: grid_token)')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, base_url: Optional[str], token: Optional[str], session_id: Optional[str], 
        config_file: Optional[str], verbose: bool):
    """GridAPI command-line interface (version {}).

    Configuration is loaded from a 'grid_token' file by default.
    Command line options override config file values.

    Example grid_token file:
        grid_token=your-api-token-here
        base_url=https://your-api-url.com

            Available commands:
                studies: list, get, create, summary, procedures, subjects, events
                studies: event-details, subject-contacts, subject-events, procedure-events
                actions: list

    All list commands support --format json for JSON output.

    Examples:
        gridapi studies list
        gridapi studies summary 100
        gridapi studies subjects 100 --format json
        gridapi studies subject-events 100 1000
        gridapi studies procedure-events 100 2249
        gridapi studies create --description "My Study"
    """.format(__version__)
    
    ctx.ensure_object(dict)
    ctx.obj['base_url'] = base_url
    ctx.obj['token'] = token
    ctx.obj['session_id'] = session_id
    ctx.obj['config_file'] = config_file
    ctx.obj['verbose'] = verbose


@cli.command('config')
@click.option('--show-token', is_flag=True, help='Show the token value (otherwise masked)')
@click.pass_context
def show_config(ctx, show_token: bool):
    """Show current configuration."""
    config = load_config_file(ctx.obj.get('config_file'))
    
    console.print("[bold]Current Configuration:[/bold]")
    
    # Show config file values
    if config:
        console.print("\n[bold blue]From config file:[/bold blue]")
        for key, value in config.items():
            if key == 'grid_token' and not show_token:
                console.print(f"  {key}=***masked***")
            else:
                console.print(f"  {key}={value}")
    else:
        console.print("\n[yellow]No config file found[/yellow]")
    
    # Show command line overrides
    overrides = []
    if ctx.obj.get('base_url'):
        overrides.append(f"base_url={ctx.obj['base_url']}")
    if ctx.obj.get('token'):
        token_value = ctx.obj['token'] if show_token else "***masked***"
        overrides.append(f"token={token_value}")
    if ctx.obj.get('session_id'):
        overrides.append(f"session_id={ctx.obj['session_id']}")
    
    if overrides:
        console.print("\n[bold green]Command line overrides:[/bold green]")
        for override in overrides:
            console.print(f"  {override}")
    
    # Show final resolved values
    try:
        client = get_client_from_context(ctx)
        console.print("\n[bold cyan]Final resolved values:[/bold cyan]")
        console.print(f"  base_url={client.base_url}")
        if client.auth.token:
            token_value = client.auth.token if show_token else "***masked***"
            console.print(f"  token={token_value}")
        if client.auth.session_id:
            console.print(f"  session_id={client.auth.session_id}")
    except SystemExit:
        console.print("\n[red]Error: Could not resolve configuration[/red]")


@cli.group()
def studies():
    """Study management commands."""
    pass


@studies.command('list')
@click.option('--investigator', help='Filter by investigator')
@click.option('--status', type=int, help='Filter by status')
@click.option('--search', help='Search term')
@click.option('--format', 'output_format', type=click.Choice(['table', 'json']), default='table')
@click.pass_context
def list_studies(ctx, investigator: Optional[str], status: Optional[int], 
                search: Optional[str], output_format: str):
    """List studies."""
    try:
        client = get_client_from_context(ctx)
        
        studies = client.grid.studies.list(
            investigator=investigator,
            status=status,
            search=search
        )
        
        if output_format == 'json':
            console.print(JSON(json.dumps([study.dict() for study in studies], default=str)))
        else:
            table = Table(title="Studies")
            table.add_column("ID", style="cyan")
            table.add_column("Description", style="magenta")
            table.add_column("Investigator", style="green")
            table.add_column("Status", style="yellow")
            
            for study in studies:
                table.add_row(
                    str(study.id),
                    study.description or "",
                    study.investigator or "",
                    str(study.status) if study.status else ""
                )
            
            console.print(table)
    
    except GridAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@studies.command('get')
@click.argument('study_id', type=int)
@click.option('--format', 'output_format', type=click.Choice(['table', 'json']), default='json')
@click.pass_context
def get_study(ctx, study_id: int, output_format: str):
    """Get a specific study."""
    try:
        client = get_client_from_context(ctx)
        
        study = client.grid.studies.get(study_id)
        
        if output_format == 'json':
            console.print(JSON(study.json()))
        else:
            table = Table(title=f"Study {study_id}")
            table.add_column("Field", style="cyan")
            table.add_column("Value", style="magenta")
            
            for field, value in study.dict().items():
                table.add_row(field, str(value) if value is not None else "")
            
            console.print(table)
    
    except GridAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@studies.command('create')
@click.option('--description', required=True, help='Study description')
@click.option('--investigator', help='Principal investigator')
@click.option('--status', type=int, help='Study status')
@click.option('--note', help='Study notes')
@click.pass_context
def create_study(ctx, description: str, investigator: Optional[str], 
                status: Optional[int], note: Optional[str]):
    """Create a new study."""
    try:
        client = get_client_from_context(ctx)
        
        study_data = {
            'description': description,
            'investigator': investigator,
            'status': status,
            'note': note
        }
        
        study = client.grid.studies.create(study_data)
        console.print(f"[green]Created study {study.id}[/green]")
        console.print(JSON(study.json()))
    
    except GridAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@studies.command('procedures')
@click.argument('study_id', type=int)
@click.option('--format', 'output_format', type=click.Choice(['table', 'json']), default='table')
@click.pass_context
def list_study_procedures(ctx, study_id: int, output_format: str):
    """List procedures for a specific study."""
    try:
        client = get_client_from_context(ctx)
        
        # Get raw data and inject study_id
        raw_procedures = client.request("GET", f"/api/grid/studies/{study_id}/procedures/")
        
        # Inject study_id into each procedure
        procedures_data = []
        for proc in raw_procedures:
            proc['study_id'] = study_id
            procedures_data.append(proc)
        
        if output_format == 'json':
            console.print(JSON(json.dumps(procedures_data, default=str)))
        else:
            table = Table(title=f"Procedures for Study {study_id}")
            table.add_column("ID", style="cyan")
            table.add_column("Description", style="green")
            table.add_column("Note", style="yellow")
            table.add_column("Contact Info", style="blue")
            table.add_column("Created At", style="red")
            table.add_column("Created By", style="magenta")
            
            for proc in procedures_data:
                # Format created_at timestamp
                created_at = proc.get('created_at')
                if created_at:
                    # Extract just the date part for cleaner display
                    created_display = str(created_at).split('T')[0]
                else:
                    created_display = "N/A"
                
                table.add_row(
                    str(proc.get('id', 'N/A')),
                    proc.get('description', 'N/A'),
                    proc.get('note', 'N/A'),
                    proc.get('contact_info', 'N/A'),
                    created_display,
                    proc.get('created_by', 'N/A')
                )
            
            console.print(table)
    
    except GridAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@studies.command('subjects')
@click.argument('study_id', type=int)
@click.option('--format', 'output_format', type=click.Choice(['table', 'json']), default='table')
@click.pass_context
def list_study_subjects(ctx, study_id: int, output_format: str):
    """List subjects for a specific study."""
    try:
        client = get_client_from_context(ctx)
        
        # Get raw data
        subjects_data = client.request("GET", f"/api/grid/studies/{study_id}/subjects/")
        
        if output_format == 'json':
            console.print(JSON(json.dumps(subjects_data, default=str)))
        else:
            table = Table(title=f"Subjects for Study {study_id}")
            table.add_column("ID", style="cyan")
            table.add_column("Last Name", style="magenta")
            table.add_column("First Name", style="green")
            table.add_column("Date of Birth", style="yellow")
            table.add_column("Sex", style="blue")
            table.add_column("Created At", style="red")
            
            for subj in subjects_data:
                # Convert sex code to readable format
                sex_value = subj.get('sex')
                if sex_value == 1:
                    sex_display = "Male"
                elif sex_value == 2:
                    sex_display = "Female"
                else:
                    sex_display = str(sex_value) if sex_value is not None else "N/A"
                
                # Format created_at timestamp
                created_at = subj.get('created_at')
                if created_at:
                    # Extract just the date part for cleaner display
                    created_display = str(created_at).split('T')[0]
                else:
                    created_display = "N/A"
                
                table.add_row(
                    str(subj.get('id', 'N/A')),
                    subj.get('last_name', 'N/A'),
                    subj.get('first_name', 'N/A'),
                    str(subj.get('date_of_birth', 'N/A')),
                    sex_display,
                    created_display
                )
            
            console.print(table)
    
    except GridAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@studies.command('summary')
@click.argument('study_id', type=int)
@click.option('--format', 'output_format', type=click.Choice(['table', 'json']), default='table')
@click.pass_context
def show_study_summary(ctx, study_id: int, output_format: str):
    """Show comprehensive summary for a study including all related data."""
    try:
        client = get_client_from_context(ctx)
        
        # Get study information
        study_data = client.request("GET", f"/api/grid/studies/{study_id}/")
        
        # Get related data
        subjects_data = client.request("GET", f"/api/grid/studies/{study_id}/subjects/")
        procedures_data = client.request("GET", f"/api/grid/studies/{study_id}/procedures/")
        events_data = client.request("GET", f"/api/grid/studies/{study_id}/events/")
        
        if output_format == 'json':
            # Combine all data into a comprehensive JSON response
            comprehensive_data = {
                'study': study_data,
                'subjects': subjects_data,
                'procedures': procedures_data,
                'events': events_data,
                'summary': {
                    'total_subjects': len(subjects_data),
                    'total_procedures': len(procedures_data),
                    'total_events': len(events_data)
                }
            }
            console.print(JSON(json.dumps(comprehensive_data, default=str)))
        else:
            # Display comprehensive table format
            console.print(f"\n[bold blue]Study Details for Study {study_id}[/bold blue]")
            console.print("=" * 60)
            
            # Study basic information
            console.print(f"[bold]Study ID:[/bold] {study_data.get('id', 'N/A')}")
            console.print(f"[bold]Description:[/bold] {study_data.get('description', 'N/A')}")
            console.print(f"[bold]Note:[/bold] {study_data.get('note', 'N/A')}")
            console.print(f"[bold]Investigator:[/bold] {study_data.get('investigator', 'N/A')}")
            console.print(f"[bold]Status:[/bold] {study_data.get('status', 'N/A')}")
            console.print(f"[bold]Start Date:[/bold] {study_data.get('start_date', 'N/A')}")
            console.print(f"[bold]End Date:[/bold] {study_data.get('end_date', 'N/A')}")
            console.print(f"[bold]Created By:[/bold] {study_data.get('created_by', 'N/A')}")
            console.print(f"[bold]Updated By:[/bold] {study_data.get('updated_by', 'N/A')}")
            console.print(f"[bold]Created At:[/bold] {study_data.get('created_at', 'N/A')}")
            console.print(f"[bold]Updated At:[/bold] {study_data.get('updated_at', 'N/A')}")
            console.print(f"[bold]Lock Version:[/bold] {study_data.get('lock_version', 'N/A')}")
            
            # Summary statistics
            console.print(f"\n[bold green]Summary Statistics[/bold green]")
            console.print("-" * 30)
            console.print(f"Total Subjects: {len(subjects_data)}")
            console.print(f"Total Procedures: {len(procedures_data)}")
            console.print(f"Total Events: {len(events_data)}")
            
            # Subjects table
            if subjects_data:
                console.print(f"\n[bold yellow]Subjects ({len(subjects_data)} total)[/bold yellow]")
                subjects_table = Table()
                subjects_table.add_column("ID", style="cyan")
                subjects_table.add_column("Last Name", style="magenta")
                subjects_table.add_column("First Name", style="green")
                subjects_table.add_column("Date of Birth", style="yellow")
                subjects_table.add_column("Sex", style="blue")
                subjects_table.add_column("Created At", style="red")
                
                for subj in subjects_data:
                    # Convert sex code to readable format
                    sex_value = subj.get('sex')
                    if sex_value == 1:
                        sex_display = "Male"
                    elif sex_value == 2:
                        sex_display = "Female"
                    else:
                        sex_display = str(sex_value) if sex_value is not None else "N/A"
                    
                    # Format created_at timestamp
                    created_at = subj.get('created_at')
                    if created_at:
                        created_display = str(created_at).split('T')[0]
                    else:
                        created_display = "N/A"
                    
                    subjects_table.add_row(
                        str(subj.get('id', 'N/A')),
                        subj.get('last_name', 'N/A'),
                        subj.get('first_name', 'N/A'),
                        str(subj.get('date_of_birth', 'N/A')),
                        sex_display,
                        created_display
                    )
                
                console.print(subjects_table)
            
            # Procedures table
            if procedures_data:
                console.print(f"\n[bold yellow]Procedures ({len(procedures_data)} total)[/bold yellow]")
                procedures_table = Table()
                procedures_table.add_column("ID", style="cyan")
                procedures_table.add_column("Description", style="green")
                procedures_table.add_column("Note", style="yellow")
                procedures_table.add_column("Contact Info", style="blue")
                procedures_table.add_column("Created At", style="red")
                procedures_table.add_column("Created By", style="magenta")
                
                for proc in procedures_data:
                    # Format created_at timestamp
                    created_at = proc.get('created_at')
                    if created_at:
                        created_display = str(created_at).split('T')[0]
                    else:
                        created_display = "N/A"
                    
                    procedures_table.add_row(
                        str(proc.get('id', 'N/A')),
                        proc.get('description', 'N/A'),
                        proc.get('note', 'N/A'),
                        proc.get('contact_info', 'N/A'),
                        created_display,
                        proc.get('created_by', 'N/A')
                    )
                
                console.print(procedures_table)
            
            # Events summary (first 10 events)
            if events_data:
                console.print(f"\n[bold yellow]Recent Events (showing first 10 of {len(events_data)} total)[/bold yellow]")
                events_table = Table()
                events_table.add_column("ID", style="cyan")
                events_table.add_column("Subject", style="magenta")
                events_table.add_column("Procedure", style="green")
                events_table.add_column("Key Person", style="blue")
                events_table.add_column("Start Time", style="red")
                events_table.add_column("Status", style="white")
                events_table.add_column("Quality", style="bright_white")
                
                # Create lookups for better display
                subject_lookup = {}
                for subj in subjects_data:
                    subject_id = subj.get('id')
                    last_name = subj.get('last_name', '')
                    first_name = subj.get('first_name', '')
                    if last_name and first_name:
                        subject_lookup[subject_id] = f"{subject_id}: {last_name}, {first_name}"
                    else:
                        subject_lookup[subject_id] = f"{subject_id}: Subject {subject_id}"
                
                procedure_lookup = {}
                for proc in procedures_data:
                    procedure_lookup[proc.get('id')] = proc.get('description', 'N/A')
                
                # Show first 10 events
                for event in events_data[:10]:
                    # Format event_start_time
                    event_start_time = event.get('event_start_time')
                    if event_start_time:
                        time_display = str(event_start_time).split('T')[0]
                    else:
                        time_display = "N/A"
                    
                    # Lookup subject and procedure names
                    subject_id = event.get('subject_id')
                    subject_name = subject_lookup.get(subject_id, f'Subject {subject_id}')
                    
                    procedure_id = event.get('procedure_id')
                    procedure_name = procedure_lookup.get(procedure_id, 'N/A')
                    procedure_display = f"{procedure_id}: {procedure_name}"
                    
                    events_table.add_row(
                        str(event.get('id', 'N/A')),
                        subject_name,
                        procedure_display,
                        event.get('key_person', 'N/A'),
                        time_display,
                        str(event.get('event_status', 'N/A')),
                        str(event.get('event_quality', 'N/A'))
                    )
                
                console.print(events_table)
                
                if len(events_data) > 10:
                    console.print(f"[dim]... and {len(events_data) - 10} more events[/dim]")
                    console.print(f"[dim]Use 'gridapi studies events {study_id}' to see all events[/dim]")
    
    except GridAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@studies.command('procedure-events')
@click.argument('study_id', type=int)
@click.argument('procedure_id', type=int)
@click.option('--format', 'output_format', type=click.Choice(['table', 'json']), default='table')
@click.pass_context
def list_procedure_events(ctx, study_id: int, procedure_id: int, output_format: str):
    """List events for a specific procedure in a study."""
    try:
        client = get_client_from_context(ctx)
        
        # Get raw data
        events_data = client.request("GET", f"/api/grid/studies/{study_id}/events/")
        
        # Filter events for the specific procedure
        procedure_events = [event for event in events_data if event.get('procedure_id') == procedure_id]
        
        # Get procedures data to lookup procedure names
        procedures_data = client.request("GET", f"/api/grid/studies/{study_id}/procedures/")
        
        # Create procedure lookup dictionary
        procedure_lookup = {}
        for proc in procedures_data:
            procedure_lookup[proc.get('id')] = proc.get('description', 'N/A')
        
        # Get subjects data to lookup subject names
        subjects_data = client.request("GET", f"/api/grid/studies/{study_id}/subjects/")
        
        # Create subject lookup dictionary
        subject_lookup = {}
        for subj in subjects_data:
            subject_id = subj.get('id')
            last_name = subj.get('last_name', '')
            first_name = subj.get('first_name', '')
            if last_name and first_name:
                subject_lookup[subject_id] = f"{subject_id}: {last_name}, {first_name}"
            else:
                subject_lookup[subject_id] = f"{subject_id}: Subject {subject_id}"
        
        # Get the procedure name for the title
        procedure_name = procedure_lookup.get(procedure_id, f'Procedure {procedure_id}')
        
        if output_format == 'json':
            console.print(JSON(json.dumps(procedure_events, default=str)))
        else:
            table = Table(title=f"Events for {procedure_name} (ID: {procedure_id}) in Study {study_id}")
            table.add_column("ID", style="cyan")
            table.add_column("Subject ID", style="magenta")
            table.add_column("Procedure ID", style="green")
            table.add_column("Key Person", style="blue")
            table.add_column("Event Start Time", style="red")
            table.add_column("Event Status", style="white")
            table.add_column("Event Quality", style="bright_white")
            table.add_column("Event Note", style="bright_blue")
            
            for event in procedure_events:
                # Format event_start_time
                event_start_time = event.get('event_start_time')
                if event_start_time:
                    # Extract just the date part for cleaner display
                    time_display = str(event_start_time).split('T')[0]
                else:
                    time_display = "N/A"
                
                # Lookup procedure name
                procedure_id_from_event = event.get('procedure_id')
                procedure_name_from_lookup = procedure_lookup.get(procedure_id_from_event, 'N/A')
                procedure_display = f"{procedure_id_from_event}: {procedure_name_from_lookup}"
                
                # Lookup subject name
                subject_id = event.get('subject_id')
                subject_name = subject_lookup.get(subject_id, f'Subject {subject_id}')
                
                table.add_row(
                    str(event.get('id', 'N/A')),
                    subject_name,
                    procedure_display,
                    procedure_name_from_lookup,
                    event.get('key_person', 'N/A'),
                    time_display,
                    str(event.get('event_status', 'N/A')),
                    str(event.get('event_quality', 'N/A')),
                    event.get('event_note', 'N/A')
                )
            
            console.print(table)
    
    except GridAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@studies.command('subject-events')
@click.argument('study_id', type=int)
@click.argument('subject_id', type=int)
@click.option('--format', 'output_format', type=click.Choice(['table', 'json']), default='table')
@click.pass_context
def list_subject_events(ctx, study_id: int, subject_id: int, output_format: str):
    """List events for a specific subject in a study."""
    try:
        client = get_client_from_context(ctx)
        
        # Get raw data
        events_data = client.request("GET", f"/api/grid/studies/{study_id}/events/")
        
        # Filter events for the specific subject
        subject_events = [event for event in events_data if event.get('subject_id') == subject_id]
        
        # Get procedures data to lookup procedure names
        procedures_data = client.request("GET", f"/api/grid/studies/{study_id}/procedures/")
        
        # Create procedure lookup dictionary
        procedure_lookup = {}
        for proc in procedures_data:
            procedure_lookup[proc.get('id')] = proc.get('description', 'N/A')
        
        # Get subjects data to lookup subject names
        subjects_data = client.request("GET", f"/api/grid/studies/{study_id}/subjects/")
        
        # Create subject lookup dictionary
        subject_lookup = {}
        for subj in subjects_data:
            subject_id = subj.get('id')
            last_name = subj.get('last_name', '')
            first_name = subj.get('first_name', '')
            if last_name and first_name:
                subject_lookup[subject_id] = f"{subject_id}: {last_name}, {first_name}"
            else:
                subject_lookup[subject_id] = f"{subject_id}: Subject {subject_id}"
        
        if output_format == 'json':
            console.print(JSON(json.dumps(subject_events, default=str)))
        else:
            table = Table(title=f"Events for Subject {subject_id} in Study {study_id}")
            table.add_column("ID", style="cyan")
            table.add_column("Subject ID", style="magenta")
            table.add_column("Procedure ID", style="green")
            table.add_column("Key Person", style="blue")
            table.add_column("Event Start Time", style="red")
            table.add_column("Event Status", style="white")
            table.add_column("Event Quality", style="bright_white")
            table.add_column("Event Note", style="bright_blue")
            
            for event in subject_events:
                # Format event_start_time
                event_start_time = event.get('event_start_time')
                if event_start_time:
                    # Extract just the date part for cleaner display
                    time_display = str(event_start_time).split('T')[0]
                else:
                    time_display = "N/A"
                
                # Lookup procedure name
                procedure_id = event.get('procedure_id')
                procedure_name = procedure_lookup.get(procedure_id, 'N/A')
                procedure_display = f"{procedure_id}: {procedure_name}"
                
                # Lookup subject name
                subject_id_from_event = event.get('subject_id')
                subject_name = subject_lookup.get(subject_id_from_event, f'Subject {subject_id_from_event}')
                
                table.add_row(
                    str(event.get('id', 'N/A')),
                    subject_name,
                    procedure_display,
                    event.get('key_person', 'N/A'),
                    time_display,
                    str(event.get('event_status', 'N/A')),
                    str(event.get('event_quality', 'N/A')),
                    event.get('event_note', 'N/A')
                )
            
            console.print(table)
    
    except GridAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@studies.command('events')
@click.argument('study_id', type=int)
@click.option('--format', 'output_format', type=click.Choice(['table', 'json']), default='table')
@click.pass_context
def list_study_events(ctx, study_id: int, output_format: str):
    """List events for a specific study."""
    try:
        client = get_client_from_context(ctx)
        
        # Get raw data
        events_data = client.request("GET", f"/api/grid/studies/{study_id}/events/")
        
        # Get procedures data to lookup procedure names
        procedures_data = client.request("GET", f"/api/grid/studies/{study_id}/procedures/")
        
        # Create procedure lookup dictionary
        procedure_lookup = {}
        for proc in procedures_data:
            procedure_lookup[proc.get('id')] = proc.get('description', 'N/A')
        
        # Get subjects data to lookup subject names
        subjects_data = client.request("GET", f"/api/grid/studies/{study_id}/subjects/")
        
        # Create subject lookup dictionary
        subject_lookup = {}
        for subj in subjects_data:
            subject_id = subj.get('id')
            last_name = subj.get('last_name', '')
            first_name = subj.get('first_name', '')
            if last_name and first_name:
                subject_lookup[subject_id] = f"{subject_id}: {last_name}, {first_name}"
            else:
                subject_lookup[subject_id] = f"{subject_id}: Subject {subject_id}"
        
        if output_format == 'json':
            console.print(JSON(json.dumps(events_data, default=str)))
        else:
            table = Table(title=f"Events for Study {study_id}")
            table.add_column("ID", style="cyan")
            table.add_column("Subject ID", style="magenta")
            table.add_column("Procedure ID", style="green")
            table.add_column("Key Person", style="blue")
            table.add_column("Event Start Time", style="red")
            table.add_column("Event Status", style="white")
            table.add_column("Event Quality", style="bright_white")
            table.add_column("Event Note", style="bright_blue")
            
            for event in events_data:
                # Format event_start_time
                event_start_time = event.get('event_start_time')
                if event_start_time:
                    # Extract just the date part for cleaner display
                    time_display = str(event_start_time).split('T')[0]
                else:
                    time_display = "N/A"
                
                # Lookup procedure name
                procedure_id = event.get('procedure_id')
                procedure_name = procedure_lookup.get(procedure_id, 'N/A')
                procedure_display = f"{procedure_id}: {procedure_name}"
                
                # Lookup subject name
                subject_id_from_event = event.get('subject_id')
                subject_name = subject_lookup.get(subject_id_from_event, f'Subject {subject_id_from_event}')
                
                table.add_row(
                    str(event.get('id', 'N/A')),
                    subject_name,
                    procedure_display,
                    event.get('key_person', 'N/A'),
                    time_display,
                    str(event.get('event_status', 'N/A')),
                    str(event.get('event_quality', 'N/A')),
                    event.get('event_note', 'N/A')
                )
            
            console.print(table)
    
    except GridAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@studies.command('event-details')
@click.argument('study_id', type=int)
@click.argument('event_id', type=int)
@click.option('--format', 'output_format', type=click.Choice(['table', 'json']), default='table')
@click.pass_context
def list_event_details(ctx, study_id: int, event_id: int, output_format: str):
    """List details for a specific event."""
    try:
        client = get_client_from_context(ctx)
        
        # Get raw data
        details_data = client.request("GET", f"/api/grid/studies/{study_id}/events/{event_id}/details/")
        
        if output_format == 'json':
            console.print(JSON(json.dumps(details_data, default=str)))
        else:
            table = Table(title=f"Event Details for Event {event_id} in Study {study_id}")
            table.add_column("ID", style="cyan")
            table.add_column("Description", style="green")
            table.add_column("Data Type ID", style="magenta")
            table.add_column("JSON Data", style="yellow")
            table.add_column("Prior Detail ID", style="blue")
            table.add_column("Created By", style="red")
            table.add_column("Updated At", style="white")
            
            for detail in details_data:
                # Extract JSON data for display
                json_data = detail.get('json_data', {})
                json_display = str(json_data) if json_data else 'N/A'
                
                # Format updated_at timestamp
                updated_at = detail.get('updated_at')
                if updated_at:
                    updated_display = str(updated_at).split('T')[0]
                else:
                    updated_display = 'N/A'
                
                table.add_row(
                    str(detail.get('id', 'N/A')),
                    detail.get('description', 'N/A'),
                    str(detail.get('datatype_id', 'N/A')),
                    json_display,
                    str(detail.get('prior_detail_id', 'N/A')),
                    detail.get('created_by', 'N/A'),
                    updated_display
                )
            
            console.print(table)
    
    except GridAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@studies.command('subject-contacts')
@click.argument('study_id', type=int)
@click.argument('subject_id', type=int)
@click.option('--format', 'output_format', type=click.Choice(['table', 'json']), default='table')
@click.pass_context
def list_subject_contacts(ctx, study_id: int, subject_id: int, output_format: str):
    """List contacts for a specific subject."""
    try:
        client = get_client_from_context(ctx)
        
        # Get raw data
        contacts_data = client.request("GET", f"/api/grid/studies/{study_id}/subjects/{subject_id}/contacts/")
        
        if output_format == 'json':
            console.print(JSON(json.dumps(contacts_data, default=str)))
        else:
            table = Table(title=f"Contacts for Subject {subject_id} in Study {study_id}")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="magenta")
            table.add_column("Phone", style="green")
            table.add_column("Email", style="yellow")
            table.add_column("Address", style="blue")
            
            for contact in contacts_data:
                table.add_row(
                    str(contact.get('id', 'N/A')),
                    contact.get('name', 'N/A'),
                    contact.get('phone', 'N/A'),
                    contact.get('email', 'N/A'),
                    contact.get('address', 'N/A')
                )
            
            console.print(table)
    
    except GridAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.group()
def images():
    """Image management commands."""
    pass


@images.command('list')
@click.option('--status', help='Filter by status')
@click.option('--format', 'output_format', type=click.Choice(['table', 'json']), default='table')
@click.pass_context
def list_actions(ctx, status: Optional[str], output_format: str):
    """List image actions."""
    try:
        client = get_client_from_context(ctx)
        
        actions = client.image.actions.list(status=status)
        
        if output_format == 'json':
            console.print(JSON(json.dumps([action.dict() for action in actions], default=str)))
        else:
            table = Table(title="Image Actions")
            table.add_column("ID", style="cyan")
            table.add_column("Status", style="magenta")
            table.add_column("Start Time", style="green")
            table.add_column("Finish Time", style="yellow")
            
            for action in actions:
                table.add_row(
                    str(action.id),
                    action.status,
                    action.starttime.isoformat() if action.starttime else "",
                    action.finishtime.isoformat() if action.finishtime else ""
                )
            
            console.print(table)
    
    except GridAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    cli()


if __name__ == '__main__':
    main()
