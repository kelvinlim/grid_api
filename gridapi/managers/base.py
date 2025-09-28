"""
Base manager class for GridAPI resources.
"""

from typing import Any, Dict, List, Optional, Type, TypeVar, Union, TYPE_CHECKING
from abc import ABC, abstractmethod

from ..query import QueryBuilder
from ..exceptions import NotFoundError

if TYPE_CHECKING:
    from ..client import BaseClient

T = TypeVar('T')


class BaseManager(ABC):
    """Base manager class for API resources."""
    
    def __init__(self, client: "BaseClient"):
        """Initialize the manager with a client."""
        self.client = client
    
    @property
    @abstractmethod
    def endpoint(self) -> str:
        """Get the base endpoint for this resource."""
        pass
    
    @property
    @abstractmethod
    def model_class(self) -> Type[T]:
        """Get the model class for this resource."""
        pass
    
    def _build_endpoint(self, resource_id: Optional[int] = None, sub_path: Optional[str] = None) -> str:
        """Build the full endpoint path."""
        endpoint = self.endpoint
        
        if resource_id is not None:
            endpoint = f"{endpoint}/{resource_id}"
        
        if sub_path:
            endpoint = f"{endpoint}/{sub_path}"
        
        return endpoint
    
    def _parse_response(self, data: Any) -> Union[T, List[T], Dict[str, Any]]:
        """Parse API response data."""
        if data is None:
            return None
        
        if isinstance(data, list):
            return [self.model_class(**item) for item in data]
        elif isinstance(data, dict):
            if 'results' in data:
                # Paginated response
                return {
                    'count': data.get('count', 0),
                    'next': data.get('next'),
                    'previous': data.get('previous'),
                    'results': [self.model_class(**item) for item in data.get('results', [])]
                }
            else:
                # Single resource
                return self.model_class(**data)
        
        return data
    
    def list(
        self,
        query: Optional[QueryBuilder] = None,
        **filters
    ) -> Union[List[T], Dict[str, Any]]:
        """
        List resources with optional filtering and pagination.
        
        Args:
            query: Query builder for complex queries
            **filters: Simple filter parameters
            
        Returns:
            List of resources or paginated response
        """
        params = {}
        
        if query:
            params.update(query.build())
        
        # Add simple filters
        for key, value in filters.items():
            if value is not None:
                params[key] = value
        
        data = self.client.get(self.endpoint, params=params)
        return self._parse_response(data)
    
    def get(self, resource_id: int) -> T:
        """
        Get a single resource by ID.
        
        Args:
            resource_id: Resource ID
            
        Returns:
            Resource instance
            
        Raises:
            NotFoundError: If resource is not found
        """
        endpoint = self._build_endpoint(resource_id)
        data = self.client.get(endpoint)
        
        if data is None:
            raise NotFoundError(f"Resource with ID {resource_id} not found")
        
        return self._parse_response(data)
    
    def create(self, data: Union[Dict[str, Any], T]) -> T:
        """
        Create a new resource.
        
        Args:
            data: Resource data
            
        Returns:
            Created resource instance
        """
        if hasattr(data, 'to_dict'):
            data = data.to_dict()
        
        response_data = self.client.post(self.endpoint, data=data)
        parsed_response = self._parse_response(response_data)
        
        # Handle case where API returns a list instead of single object
        if isinstance(parsed_response, list) and len(parsed_response) > 0:
            # Return the last item (most recently created)
            return parsed_response[-1]
        
        return parsed_response
    
    def update(self, resource_id: int, data: Union[Dict[str, Any], T]) -> T:
        """
        Update an existing resource.
        
        Args:
            resource_id: Resource ID
            data: Updated resource data
            
        Returns:
            Updated resource instance
        """
        if hasattr(data, 'to_dict'):
            data = data.to_dict()
        
        endpoint = self._build_endpoint(resource_id)
        response_data = self.client.put(endpoint, data=data)
        return self._parse_response(response_data)
    
    def delete(self, resource_id: int) -> bool:
        """
        Delete a resource.
        
        Args:
            resource_id: Resource ID
            
        Returns:
            True if successful
        """
        endpoint = self._build_endpoint(resource_id)
        self.client.delete(endpoint)
        return True
    
    def search(self, term: str, **filters) -> Union[List[T], Dict[str, Any]]:
        """
        Search resources.
        
        Args:
            term: Search term
            **filters: Additional filters
            
        Returns:
            Search results
        """
        query = QueryBuilder().search(term)
        
        # Add additional filters
        for key, value in filters.items():
            if value is not None:
                query.filter(key, value)
        
        return self.list(query=query)
    
    def filter(self, **filters) -> Union[List[T], Dict[str, Any]]:
        """
        Filter resources.
        
        Args:
            **filters: Filter parameters
            
        Returns:
            Filtered results
        """
        query = QueryBuilder()
        
        for key, value in filters.items():
            if value is not None:
                query.filter(key, value)
        
        return self.list(query=query)
    
    def order_by(self, field: str, ascending: bool = True) -> Union[List[T], Dict[str, Any]]:
        """
        Order resources.
        
        Args:
            field: Field to order by
            ascending: Whether to order ascending
            
        Returns:
            Ordered results
        """
        query = QueryBuilder().order_by(field, ascending)
        return self.list(query=query)
