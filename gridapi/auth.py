"""
Authentication handling for GridAPI client.
"""

from typing import Optional, Dict, Any
from .exceptions import AuthenticationError


class AuthHandler:
    """Handles authentication for GridAPI requests."""
    
    def __init__(self, token: Optional[str] = None, session_id: Optional[str] = None):
        """
        Initialize authentication handler.
        
        Args:
            token: API token for token-based authentication
            session_id: Session ID for cookie-based authentication
        """
        if not token and not session_id:
            raise AuthenticationError("Either token or session_id must be provided")
        
        self.token = token
        self.session_id = session_id
    
    def get_headers(self) -> Dict[str, str]:
        """Get authentication headers for requests."""
        headers = {}
        
        if self.token:
            headers["X-API-Key"] = self.token
        
        return headers
    
    def get_cookies(self) -> Dict[str, str]:
        """Get authentication cookies for requests."""
        cookies = {}
        
        if self.session_id:
            cookies["sessionid"] = self.session_id
        
        return cookies
    
    def is_authenticated(self) -> bool:
        """Check if authentication is properly configured."""
        return bool(self.token or self.session_id)
