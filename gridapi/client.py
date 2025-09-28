"""
Main GridAPI client classes.
"""

import json
import logging
from typing import Any, Dict, Optional, Union
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .auth import AuthHandler
from .exceptions import (
    GridAPIError,
    ValidationError,
    AuthenticationError,
    NotFoundError,
    ServerError,
    RateLimitError,
    ConnectionError,
)
from .managers import GridManager, ImageManager, TaskflowManager

logger = logging.getLogger(__name__)


class BaseClient:
    """Base client class with common functionality."""
    
    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        session_id: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ):
        """
        Initialize the base client.
        
        Args:
            base_url: Base URL of the Grid API
            token: API token for authentication
            session_id: Session ID for cookie-based authentication
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            backoff_factor: Backoff factor for retry strategy
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.auth = AuthHandler(token=token, session_id=session_id)
        
        # Setup session with retry strategy
        self.session = requests.Session()
        
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })
        
        # Add authentication headers
        self.session.headers.update(self.auth.get_headers())
        
        # Add cookies if using session authentication
        if self.auth.session_id:
            self.session.cookies.update(self.auth.get_cookies())
    
    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint."""
        return urljoin(self.base_url, endpoint.lstrip('/'))
    
    def _handle_response(self, response: requests.Response) -> Any:
        """Handle API response and raise appropriate exceptions."""
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self._handle_http_error(response, e)
        
        # Handle empty responses
        if not response.content:
            return None
        
        try:
            return response.json()
        except json.JSONDecodeError:
            return response.text
    
    def _handle_http_error(self, response: requests.Response, error: requests.exceptions.HTTPError):
        """Handle HTTP errors and raise appropriate exceptions."""
        status_code = response.status_code
        
        try:
            error_data = response.json()
            message = error_data.get('detail', error_data.get('message', str(error)))
        except (json.JSONDecodeError, KeyError):
            message = str(error)
        
        if status_code == 401:
            raise AuthenticationError(f"Authentication failed: {message}")
        elif status_code == 404:
            raise NotFoundError(f"Resource not found: {message}")
        elif status_code == 422:
            raise ValidationError(f"Validation error: {message}")
        elif status_code == 429:
            raise RateLimitError(f"Rate limit exceeded: {message}")
        elif 500 <= status_code < 600:
            raise ServerError(f"Server error ({status_code}): {message}")
        else:
            raise GridAPIError(f"API error ({status_code}): {message}", status_code)
    
    def request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Any:
        """
        Make a request to the API.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request data
            params: Query parameters
            **kwargs: Additional arguments for requests
            
        Returns:
            API response data
        """
        url = self._build_url(endpoint)
        
        # Prepare request data
        json_data = None
        if data is not None:
            json_data = data
        
        # Make request
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=json_data,
                params=params,
                timeout=self.timeout,
                **kwargs
            )
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"Connection failed: {e}")
        except requests.exceptions.Timeout as e:
            raise GridAPIError(f"Request timeout: {e}")
        except requests.exceptions.RequestException as e:
            raise GridAPIError(f"Request failed: {e}")
        
        return self._handle_response(response)
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        """Make a GET request."""
        return self.request('GET', endpoint, params=params, **kwargs)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        """Make a POST request."""
        return self.request('POST', endpoint, data=data, **kwargs)
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        """Make a PUT request."""
        return self.request('PUT', endpoint, data=data, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> Any:
        """Make a DELETE request."""
        return self.request('DELETE', endpoint, **kwargs)
    
    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        """Make a PATCH request."""
        return self.request('PATCH', endpoint, data=data, **kwargs)


class GridAPIClient(BaseClient):
    """Main GridAPI client class."""
    
    def __init__(self, *args, **kwargs):
        """Initialize the GridAPI client."""
        super().__init__(*args, **kwargs)
        
        # Initialize managers
        self.grid = GridManager(self)
        self.image = ImageManager(self)
        self.taskflow = TaskflowManager(self)
    
    def __repr__(self) -> str:
        """String representation of the client."""
        return f"GridAPIClient(base_url='{self.base_url}')"


class AsyncGridAPIClient:
    """Async version of GridAPI client (placeholder for future implementation)."""
    
    def __init__(self, *args, **kwargs):
        """Initialize the async GridAPI client."""
        # This would be implemented with aiohttp
        raise NotImplementedError("Async support will be implemented in a future version")
