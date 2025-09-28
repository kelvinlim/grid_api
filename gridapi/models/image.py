"""
Image API data models.
"""

from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import Field, validator

from .base import BaseModel, StudyRelatedModel


class Acquisition(StudyRelatedModel):
    """Image acquisition model."""
    
    id: int = Field(..., description="Acquisition ID", read_only=True)
    studyinstanceuid: str = Field(..., max_length=100, description="Study instance UID")
    accession: str = Field(..., max_length=100, description="Accession number")
    receipt: datetime = Field(..., description="Receipt timestamp")
    
    @validator('studyinstanceuid', 'accession')
    def validate_required_strings(cls, v):
        """Validate required string fields are not empty."""
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()


class Action(BaseModel):
    """Image processing action model."""
    
    id: int = Field(..., description="Action ID", read_only=True)
    acquisition: int = Field(..., description="Acquisition ID")
    starttime: datetime = Field(..., description="Action start time")
    finishtime: datetime = Field(..., description="Action finish time")
    status: str = Field(..., max_length=100, description="Action status")
    json_data: Optional[Dict[str, Any]] = Field(None, description="Additional JSON data")
    
    @validator('acquisition')
    def validate_acquisition_id(cls, v):
        """Validate acquisition ID is positive."""
        if v <= 0:
            raise ValueError('Acquisition ID must be positive')
        return v
    
    @validator('finishtime')
    def validate_finish_time(cls, v, values):
        """Validate finish time is after start time."""
        if 'starttime' in values and v <= values['starttime']:
            raise ValueError('Finish time must be after start time')
        return v


class ActionType(BaseModel):
    """Action type model."""
    
    id: int = Field(..., description="Action type ID", read_only=True)
    label: str = Field(..., max_length=100, description="Short label")
    description: str = Field(..., max_length=100, description="Description")
    json_data: Optional[Dict[str, Any]] = Field(None, description="Additional JSON data")
    
    @validator('label', 'description')
    def validate_required_strings(cls, v):
        """Validate required string fields are not empty."""
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()


class Destination(StudyRelatedModel):
    """Image destination model."""
    
    id: int = Field(..., description="Destination ID", read_only=True)
    name: Optional[str] = Field(None, description="Destination name")
    path: Optional[str] = Field(None, description="Destination path")
    json_data: Optional[Dict[str, Any]] = Field(None, description="Additional JSON data")


class RawDataIn(StudyRelatedModel):
    """Raw data input model."""
    
    id: int = Field(..., description="Raw data ID", read_only=True)
    studyinstanceuid: str = Field(..., max_length=100, description="Study instance UID")
    accession: str = Field(..., max_length=100, description="Accession number")
    receivetime: datetime = Field(..., description="Receive timestamp")
    grid_match: bool = Field(..., description="Grid match status")
    acquisition: int = Field(..., description="Acquisition ID")
    scannertype: int = Field(..., description="Scanner type ID")
    
    @validator('studyinstanceuid', 'accession')
    def validate_required_strings(cls, v):
        """Validate required string fields are not empty."""
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()
    
    @validator('acquisition', 'scannertype')
    def validate_ids(cls, v):
        """Validate IDs are positive."""
        if v <= 0:
            raise ValueError('ID must be positive')
        return v


class ScannerType(BaseModel):
    """Scanner type model."""
    
    id: int = Field(..., description="Scanner type ID", read_only=True)
    label: str = Field(..., max_length=100, description="Short label")
    cmrr_name: Optional[str] = Field(None, max_length=100, description="CMRR name")
    description: str = Field(..., max_length=100, description="Description")
    json_data: Optional[Dict[str, Any]] = Field(None, description="Additional JSON data")
    
    @validator('label', 'description')
    def validate_required_strings(cls, v):
        """Validate required string fields are not empty."""
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()
