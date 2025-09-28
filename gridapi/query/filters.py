"""
Filter and ordering utilities for GridAPI queries.
"""

from enum import Enum
from typing import Any, Optional, Union
from dataclasses import dataclass


class FilterOperator(Enum):
    """Filter operators."""
    EQUALS = "exact"
    CONTAINS = "icontains"
    STARTS_WITH = "istartswith"
    ENDS_WITH = "iendswith"
    GREATER_THAN = "gt"
    GREATER_THAN_OR_EQUAL = "gte"
    LESS_THAN = "lt"
    LESS_THAN_OR_EQUAL = "lte"
    IN = "in"
    IS_NULL = "isnull"
    IS_NOT_NULL = "isnull"


@dataclass
class Filter:
    """Represents a single filter condition."""
    
    field: str
    operator: FilterOperator
    value: Any
    
    def to_param(self) -> tuple[str, Any]:
        """Convert filter to query parameter tuple."""
        if self.operator == FilterOperator.EQUALS:
            return self.field, self.value
        elif self.operator == FilterOperator.IS_NULL:
            return f"{self.field}__isnull", True
        elif self.operator == FilterOperator.IS_NOT_NULL:
            return f"{self.field}__isnull", False
        else:
            return f"{self.field}__{self.operator.value}", self.value


@dataclass
class Ordering:
    """Represents ordering for query results."""
    
    field: str
    ascending: bool = True
    
    def to_param(self) -> str:
        """Convert ordering to query parameter."""
        if self.ascending:
            return self.field
        else:
            return f"-{self.field}"


class FilterBuilder:
    """Builder for creating complex filter conditions."""
    
    def __init__(self):
        """Initialize the filter builder."""
        self._filters: list[Filter] = []
    
    def exact(self, field: str, value: Any) -> "FilterBuilder":
        """Add exact match filter."""
        self._filters.append(Filter(field, FilterOperator.EQUALS, value))
        return self
    
    def contains(self, field: str, value: str) -> "FilterBuilder":
        """Add contains filter (case-insensitive)."""
        self._filters.append(Filter(field, FilterOperator.CONTAINS, value))
        return self
    
    def starts_with(self, field: str, value: str) -> "FilterBuilder":
        """Add starts with filter (case-insensitive)."""
        self._filters.append(Filter(field, FilterOperator.STARTS_WITH, value))
        return self
    
    def ends_with(self, field: str, value: str) -> "FilterBuilder":
        """Add ends with filter (case-insensitive)."""
        self._filters.append(Filter(field, FilterOperator.ENDS_WITH, value))
        return self
    
    def gt(self, field: str, value: Any) -> "FilterBuilder":
        """Add greater than filter."""
        self._filters.append(Filter(field, FilterOperator.GREATER_THAN, value))
        return self
    
    def gte(self, field: str, value: Any) -> "FilterBuilder":
        """Add greater than or equal filter."""
        self._filters.append(Filter(field, FilterOperator.GREATER_THAN_OR_EQUAL, value))
        return self
    
    def lt(self, field: str, value: Any) -> "FilterBuilder":
        """Add less than filter."""
        self._filters.append(Filter(field, FilterOperator.LESS_THAN, value))
        return self
    
    def lte(self, field: str, value: Any) -> "FilterBuilder":
        """Add less than or equal filter."""
        self._filters.append(Filter(field, FilterOperator.LESS_THAN_OR_EQUAL, value))
        return self
    
    def in_list(self, field: str, values: list[Any]) -> "FilterBuilder":
        """Add in list filter."""
        self._filters.append(Filter(field, FilterOperator.IN, values))
        return self
    
    def is_null(self, field: str) -> "FilterBuilder":
        """Add is null filter."""
        self._filters.append(Filter(field, FilterOperator.IS_NULL, True))
        return self
    
    def is_not_null(self, field: str) -> "FilterBuilder":
        """Add is not null filter."""
        self._filters.append(Filter(field, FilterOperator.IS_NOT_NULL, True))
        return self
    
    def build(self) -> dict[str, Any]:
        """Build the filter parameters."""
        params = {}
        for filter_obj in self._filters:
            key, value = filter_obj.to_param()
            params[key] = value
        return params
    
    def clear(self) -> "FilterBuilder":
        """Clear all filters."""
        self._filters.clear()
        return self
