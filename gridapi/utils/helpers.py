"""
Helper functions for GridAPI.
"""

from datetime import datetime, date
from typing import Any, Optional, Union


def format_datetime(dt: Optional[Union[datetime, date, str]]) -> Optional[str]:
    """
    Format datetime for API requests.
    
    Args:
        dt: Datetime, date, or string to format
        
    Returns:
        Formatted datetime string or None
    """
    if dt is None:
        return None
    
    if isinstance(dt, str):
        return dt
    
    if isinstance(dt, date) and not isinstance(dt, datetime):
        return dt.isoformat()
    
    if isinstance(dt, datetime):
        return dt.isoformat()
    
    return str(dt)


def parse_datetime(dt_str: Optional[str]) -> Optional[datetime]:
    """
    Parse datetime string from API response.
    
    Args:
        dt_str: Datetime string to parse
        
    Returns:
        Parsed datetime or None
    """
    if not dt_str:
        return None
    
    try:
        # Try parsing ISO format
        return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    except ValueError:
        try:
            # Try parsing with different formats
            for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d']:
                try:
                    return datetime.strptime(dt_str, fmt)
                except ValueError:
                    continue
        except ValueError:
            pass
    
    return None


def format_date(d: Optional[Union[date, datetime, str]]) -> Optional[str]:
    """
    Format date for API requests.
    
    Args:
        d: Date, datetime, or string to format
        
    Returns:
        Formatted date string or None
    """
    if d is None:
        return None
    
    if isinstance(d, str):
        return d
    
    if isinstance(d, datetime):
        return d.date().isoformat()
    
    if isinstance(d, date):
        return d.isoformat()
    
    return str(d)


def parse_date(d_str: Optional[str]) -> Optional[date]:
    """
    Parse date string from API response.
    
    Args:
        d_str: Date string to parse
        
    Returns:
        Parsed date or None
    """
    if not d_str:
        return None
    
    try:
        # Try parsing ISO format
        return datetime.fromisoformat(d_str).date()
    except ValueError:
        try:
            # Try parsing with different formats
            for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S']:
                try:
                    return datetime.strptime(d_str, fmt).date()
                except ValueError:
                    continue
        except ValueError:
            pass
    
    return None


def clean_dict(data: dict) -> dict:
    """
    Clean dictionary by removing None values and empty strings.
    
    Args:
        data: Dictionary to clean
        
    Returns:
        Cleaned dictionary
    """
    cleaned = {}
    for key, value in data.items():
        if value is not None and value != "":
            if isinstance(value, dict):
                cleaned_value = clean_dict(value)
                if cleaned_value:  # Only add non-empty dicts
                    cleaned[key] = cleaned_value
            elif isinstance(value, list):
                cleaned_value = [v for v in value if v is not None and v != ""]
                if cleaned_value:  # Only add non-empty lists
                    cleaned[key] = cleaned_value
            else:
                cleaned[key] = value
    
    return cleaned


def build_query_string(params: dict) -> str:
    """
    Build query string from parameters.
    
    Args:
        params: Parameters dictionary
        
    Returns:
        Query string
    """
    if not params:
        return ""
    
    query_parts = []
    for key, value in params.items():
        if value is not None:
            if isinstance(value, list):
                value = ",".join(str(v) for v in value)
            query_parts.append(f"{key}={value}")
    
    return "&".join(query_parts)
