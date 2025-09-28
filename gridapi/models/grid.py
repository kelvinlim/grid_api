"""
Grid API data models.
"""

from datetime import date, datetime
from typing import Any, Dict, Optional
from pydantic import Field, validator

from .base import BaseModel, TimestampedModel, StudyRelatedModel


class Study(TimestampedModel):
    """Study model."""
    
    id: int = Field(..., description="Study ID", read_only=True)
    description: Optional[str] = Field(None, max_length=255, description="Study description")
    note: Optional[str] = Field(None, description="Study notes")
    investigator: Optional[str] = Field(None, max_length=255, description="Principal investigator")
    status: Optional[int] = Field(None, description="Study status")
    start_date: Optional[date] = Field(None, description="Study start date")
    end_date: Optional[date] = Field(None, description="Study end date")
    
    @validator('end_date')
    def validate_end_date(cls, v, values):
        """Validate end date is after start date."""
        if v and 'start_date' in values and values['start_date']:
            # Handle placeholder dates like '0001-01-01'
            if v.year <= 1900:
                return None  # Treat placeholder dates as None
            if v < values['start_date']:
                raise ValueError('End date must be after start date')
        return v


class Datatype(TimestampedModel, StudyRelatedModel):
    """Data type model."""
    
    id: int = Field(..., description="Data type ID", read_only=True)
    name: Optional[str] = Field(None, max_length=255, description="Data type name")
    description: Optional[str] = Field(None, description="Data type description")
    json_data: Optional[Dict[str, Any]] = Field(None, description="Additional JSON data")


class SubjectStudy(TimestampedModel):
    """Subject study relationship model."""
    
    id: int = Field(..., description="Subject study ID", read_only=True)
    subject_id: int = Field(..., description="Subject ID")
    study_id: int = Field(..., description="Study ID")
    note: Optional[str] = Field(None, description="Notes")
    study_of_origin: Optional[int] = Field(None, description="Original study ID")
    study_entry_date: Optional[date] = Field(None, description="Study entry date")
    participant_status: Optional[int] = Field(None, description="Participant status")
    group_id: Optional[int] = Field(None, description="Group ID")
    
    @validator('subject_id', 'study_id')
    def validate_ids(cls, v):
        """Validate IDs are positive."""
        if v <= 0:
            raise ValueError('ID must be positive')
        return v


class StudyEvent(BaseModel):
    """Study event model."""
    
    id: int = Field(..., description="Event ID", read_only=True)
    study_id: int = Field(..., description="Study ID")
    name: Optional[str] = Field(None, description="Event name")
    description: Optional[str] = Field(None, description="Event description")
    event_date: Optional[date] = Field(None, description="Event date")
    json_data: Optional[Dict[str, Any]] = Field(None, description="Additional JSON data")
    
    @validator('study_id')
    def validate_study_id(cls, v):
        """Validate study ID is positive."""
        if v <= 0:
            raise ValueError('Study ID must be positive')
        return v


class StudyEventDetail(BaseModel):
    """Study event detail model."""
    
    id: int = Field(..., description="Event detail ID", read_only=True)
    event_id: int = Field(..., description="Event ID")
    study_id: int = Field(..., description="Study ID")
    name: Optional[str] = Field(None, description="Detail name")
    description: Optional[str] = Field(None, description="Detail description")
    value: Optional[str] = Field(None, description="Detail value")
    json_data: Optional[Dict[str, Any]] = Field(None, description="Additional JSON data")
    
    @validator('event_id', 'study_id')
    def validate_ids(cls, v):
        """Validate IDs are positive."""
        if v <= 0:
            raise ValueError('ID must be positive')
        return v


class StudyProcedure(BaseModel):
    """Study procedure model."""
    
    id: int = Field(..., description="Procedure ID", read_only=True)
    study_id: int = Field(..., description="Study ID")
    name: Optional[str] = Field(None, description="Procedure name")
    description: Optional[str] = Field(None, description="Procedure description")
    procedure_date: Optional[date] = Field(None, description="Procedure date")
    json_data: Optional[Dict[str, Any]] = Field(None, description="Additional JSON data")
    
    @validator('study_id')
    def validate_study_id(cls, v):
        """Validate study ID is positive."""
        if v <= 0:
            raise ValueError('Study ID must be positive')
        return v


class StudySubject(BaseModel):
    """Study subject model."""
    
    id: int = Field(..., description="Subject ID", read_only=True)
    study_id: int = Field(..., description="Study ID")
    subject_number: Optional[str] = Field(None, description="Subject number")
    first_name: Optional[str] = Field(None, description="First name")
    last_name: Optional[str] = Field(None, description="Last name")
    date_of_birth: Optional[date] = Field(None, description="Date of birth")
    gender: Optional[str] = Field(None, description="Gender")
    json_data: Optional[Dict[str, Any]] = Field(None, description="Additional JSON data")
    
    @validator('study_id')
    def validate_study_id(cls, v):
        """Validate study ID is positive."""
        if v <= 0:
            raise ValueError('Study ID must be positive')
        return v


class StudySubjectContact(BaseModel):
    """Study subject contact model."""
    
    id: int = Field(..., description="Contact ID", read_only=True)
    subject_id: int = Field(..., description="Subject ID")
    study_id: int = Field(..., description="Study ID")
    contact_type: Optional[str] = Field(None, description="Contact type")
    contact_value: Optional[str] = Field(None, description="Contact value")
    is_primary: Optional[bool] = Field(False, description="Is primary contact")
    json_data: Optional[Dict[str, Any]] = Field(None, description="Additional JSON data")
    
    @validator('subject_id', 'study_id')
    def validate_ids(cls, v):
        """Validate IDs are positive."""
        if v <= 0:
            raise ValueError('ID must be positive')
        return v
