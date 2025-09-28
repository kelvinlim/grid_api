"""
Validation utilities for GridAPI.
"""

from datetime import date, datetime
from typing import Any, Optional, Union
from ..exceptions import ValidationError


def validate_study_id(study_id: Any) -> int:
    """
    Validate study ID.
    
    Args:
        study_id: Study ID to validate
        
    Returns:
        Validated study ID
        
    Raises:
        ValidationError: If study ID is invalid
    """
    if not isinstance(study_id, int):
        try:
            study_id = int(study_id)
        except (ValueError, TypeError):
            raise ValidationError(f"Study ID must be an integer, got {type(study_id).__name__}")
    
    if study_id <= 0:
        raise ValidationError("Study ID must be positive")
    
    return study_id


def validate_date_range(start_date: Optional[Union[str, date, datetime]], 
                       end_date: Optional[Union[str, date, datetime]]) -> tuple[Optional[date], Optional[date]]:
    """
    Validate date range.
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        Tuple of validated start and end dates
        
    Raises:
        ValidationError: If date range is invalid
    """
    # Convert strings to date objects if needed
    if isinstance(start_date, str):
        try:
            start_date = datetime.fromisoformat(start_date).date()
        except ValueError:
            raise ValidationError(f"Invalid start date format: {start_date}")
    
    if isinstance(end_date, str):
        try:
            end_date = datetime.fromisoformat(end_date).date()
        except ValueError:
            raise ValidationError(f"Invalid end date format: {end_date}")
    
    # Convert datetime to date if needed
    if isinstance(start_date, datetime):
        start_date = start_date.date()
    
    if isinstance(end_date, datetime):
        end_date = end_date.date()
    
    # Validate date range
    if start_date and end_date and end_date < start_date:
        raise ValidationError("End date must be after start date")
    
    return start_date, end_date


def validate_required_field(value: Any, field_name: str) -> Any:
    """
    Validate required field is not None or empty.
    
    Args:
        value: Field value to validate
        field_name: Name of the field for error messages
        
    Returns:
        Validated value
        
    Raises:
        ValidationError: If field is None or empty
    """
    if value is None:
        raise ValidationError(f"{field_name} is required")
    
    if isinstance(value, str) and not value.strip():
        raise ValidationError(f"{field_name} cannot be empty")
    
    return value


def validate_string_length(value: str, field_name: str, max_length: int) -> str:
    """
    Validate string length.
    
    Args:
        value: String value to validate
        field_name: Name of the field for error messages
        max_length: Maximum allowed length
        
    Returns:
        Validated string
        
    Raises:
        ValidationError: If string is too long
    """
    if len(value) > max_length:
        raise ValidationError(f"{field_name} must be {max_length} characters or less")
    
    return value


def validate_positive_integer(value: Any, field_name: str) -> int:
    """
    Validate positive integer.
    
    Args:
        value: Value to validate
        field_name: Name of the field for error messages
        
    Returns:
        Validated integer
        
    Raises:
        ValidationError: If value is not a positive integer
    """
    if not isinstance(value, int):
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise ValidationError(f"{field_name} must be an integer")
    
    if value <= 0:
        raise ValidationError(f"{field_name} must be positive")
    
    return value
