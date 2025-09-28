"""
Query builder for GridAPI requests.
"""

from typing import Any, Dict, List, Optional, Union
from .filters import FilterBuilder, Ordering


class QueryBuilder:
    """Builder for creating API query parameters."""
    
    def __init__(self):
        """Initialize the query builder."""
        self._search: Optional[str] = None
        self._ordering: Optional[str] = None
        self._filters: FilterBuilder = FilterBuilder()
        self._page: Optional[int] = None
        self._page_size: Optional[int] = None
    
    def search(self, term: str) -> "QueryBuilder":
        """Add search term."""
        self._search = term
        return self
    
    def order_by(self, field: str, ascending: bool = True) -> "QueryBuilder":
        """Add ordering."""
        if ascending:
            self._ordering = field
        else:
            self._ordering = f"-{field}"
        return self
    
    def order_by_multiple(self, orderings: List[Ordering]) -> "QueryBuilder":
        """Add multiple orderings."""
        if orderings:
            self._ordering = ",".join(ordering.to_param() for ordering in orderings)
        return self
    
    def filter(self, field: str, value: Any) -> "QueryBuilder":
        """Add exact match filter."""
        self._filters.exact(field, value)
        return self
    
    def filter_contains(self, field: str, value: str) -> "QueryBuilder":
        """Add contains filter."""
        self._filters.contains(field, value)
        return self
    
    def filter_gt(self, field: str, value: Any) -> "QueryBuilder":
        """Add greater than filter."""
        self._filters.gt(field, value)
        return self
    
    def filter_gte(self, field: str, value: Any) -> "QueryBuilder":
        """Add greater than or equal filter."""
        self._filters.gte(field, value)
        return self
    
    def filter_lt(self, field: str, value: Any) -> "QueryBuilder":
        """Add less than filter."""
        self._filters.lt(field, value)
        return self
    
    def filter_lte(self, field: str, value: Any) -> "QueryBuilder":
        """Add less than or equal filter."""
        self._filters.lte(field, value)
        return self
    
    def filter_in(self, field: str, values: List[Any]) -> "QueryBuilder":
        """Add in list filter."""
        self._filters.in_list(field, values)
        return self
    
    def filter_null(self, field: str) -> "QueryBuilder":
        """Add is null filter."""
        self._filters.is_null(field)
        return self
    
    def filter_not_null(self, field: str) -> "QueryBuilder":
        """Add is not null filter."""
        self._filters.is_not_null(field)
        return self
    
    def page(self, page: int) -> "QueryBuilder":
        """Set page number."""
        if page < 1:
            raise ValueError("Page number must be >= 1")
        self._page = page
        return self
    
    def page_size(self, size: int) -> "QueryBuilder":
        """Set page size."""
        if size < 1:
            raise ValueError("Page size must be >= 1")
        self._page_size = size
        return self
    
    def paginate(self, page: int, page_size: int) -> "QueryBuilder":
        """Set pagination."""
        return self.page(page).page_size(page_size)
    
    def build(self) -> Dict[str, Any]:
        """Build the query parameters."""
        params = {}
        
        # Add search
        if self._search is not None:
            params["search"] = self._search
        
        # Add ordering
        if self._ordering is not None:
            params["ordering"] = self._ordering
        
        # Add filters
        params.update(self._filters.build())
        
        # Add pagination
        if self._page is not None:
            params["page"] = self._page
        if self._page_size is not None:
            params["page_size"] = self._page_size
        
        return params
    
    def clear(self) -> "QueryBuilder":
        """Clear all query parameters."""
        self._search = None
        self._ordering = None
        self._filters.clear()
        self._page = None
        self._page_size = None
        return self
    
    def __str__(self) -> str:
        """String representation of the query."""
        params = self.build()
        if not params:
            return ""
        
        param_strings = []
        for key, value in params.items():
            if isinstance(value, list):
                value = ",".join(str(v) for v in value)
            param_strings.append(f"{key}={value}")
        
        return "&".join(param_strings)
