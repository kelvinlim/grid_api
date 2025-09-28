"""
Base model classes for GridAPI.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, TypeVar, Generic
from pydantic import BaseModel as PydanticBaseModel, Field, validator
from pydantic.types import StrictInt, StrictStr

T = TypeVar('T')


class BaseModel(PydanticBaseModel):
    """Base model class with common functionality."""
    
    class Config:
        """Pydantic configuration."""
        populate_by_name = True
        validate_assignment = True
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return self.dict(exclude_unset=True)
    
    def to_json(self) -> str:
        """Convert model to JSON string."""
        return self.json(exclude_unset=True)


class BaseListResponse(BaseModel, Generic[T]):
    """Base class for paginated list responses."""
    
    count: int = Field(..., description="Total number of items")
    next: Optional[str] = Field(None, description="URL for next page")
    previous: Optional[str] = Field(None, description="URL for previous page")
    results: List[T] = Field(..., description="List of items")
    
    def __iter__(self):
        """Make the response iterable."""
        return iter(self.results)
    
    def __len__(self):
        """Return the number of results."""
        return len(self.results)
    
    def __getitem__(self, index):
        """Allow indexing into results."""
        return self.results[index]


class TimestampedModel(BaseModel):
    """Base model with timestamp fields."""
    
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    created_by: Optional[str] = Field(None, max_length=8, description="Creator")
    updated_by: Optional[str] = Field(None, max_length=8, description="Last updater")
    lock_version: Optional[int] = Field(None, description="Lock version for optimistic locking")


class StudyRelatedModel(BaseModel):
    """Base model for study-related resources."""
    
    study: int = Field(..., description="Study ID")
    
    @validator('study')
    def validate_study_id(cls, v):
        """Validate study ID is positive."""
        if v <= 0:
            raise ValueError('Study ID must be positive')
        return v
