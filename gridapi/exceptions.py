"""
Custom exceptions for GridAPI client.
"""

from typing import Any, Dict, Optional


class GridAPIError(Exception):
    """Base exception for all GridAPI errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}


class ValidationError(GridAPIError):
    """Raised when data validation fails."""
    
    def __init__(self, message: str, field_errors: Optional[Dict[str, str]] = None):
        super().__init__(message)
        self.field_errors = field_errors or {}


class AuthenticationError(GridAPIError):
    """Raised when authentication fails."""
    pass


class NotFoundError(GridAPIError):
    """Raised when a resource is not found."""
    pass


class ServerError(GridAPIError):
    """Raised when the server returns an error."""
    pass


class RateLimitError(GridAPIError):
    """Raised when rate limit is exceeded."""
    pass


class ConnectionError(GridAPIError):
    """Raised when connection to the API fails."""
    pass
