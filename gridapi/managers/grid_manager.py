"""
Grid API resource manager.
"""

from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from ..models.grid import (
    Study,
    Datatype,
    SubjectStudy,
    StudyEvent,
    StudyEventDetail,
    StudyProcedure,
    StudySubject,
    StudySubjectContact,
)
from .base import BaseManager

if TYPE_CHECKING:
    from ..client import BaseClient


class StudyManager(BaseManager):
    """Manager for Study resources."""
    
    @property
    def endpoint(self) -> str:
        return "/api/grid/studies"
    
    @property
    def model_class(self):
        return Study
    
    def list(
        self,
        created_by: Optional[str] = None,
        description: Optional[str] = None,
        investigator: Optional[str] = None,
        note: Optional[str] = None,
        status: Optional[int] = None,
        updated_by: Optional[str] = None,
        **kwargs
    ) -> Union[List[Study], Dict[str, Any]]:
        """List studies with filtering."""
        return super().list(
            created_by=created_by,
            description=description,
            investigator=investigator,
            note=note,
            status=status,
            updated_by=updated_by,
            **kwargs
        )


class DatatypeManager(BaseManager):
    """Manager for Datatype resources."""
    
    @property
    def endpoint(self) -> str:
        return "/api/grid/datatype"
    
    @property
    def model_class(self):
        return Datatype
    
    def list(
        self,
        description: Optional[str] = None,
        name: Optional[str] = None,
        **kwargs
    ) -> Union[List[Datatype], Dict[str, Any]]:
        """List datatypes with filtering."""
        return super().list(
            description=description,
            name=name,
            **kwargs
        )


class SubjectStudyManager(BaseManager):
    """Manager for SubjectStudy resources."""
    
    @property
    def endpoint(self) -> str:
        return "/api/grid/subjectstudies"
    
    @property
    def model_class(self):
        return SubjectStudy


class StudyEventManager(BaseManager):
    """Manager for StudyEvent resources."""
    
    def __init__(self, client: "BaseClient", study_id: int):
        """Initialize with study ID."""
        super().__init__(client)
        self.study_id = study_id
    
    @property
    def endpoint(self) -> str:
        return f"/api/grid/studies/{self.study_id}/events"
    
    @property
    def model_class(self):
        return StudyEvent


class StudyEventDetailManager(BaseManager):
    """Manager for StudyEventDetail resources."""
    
    def __init__(self, client: "BaseClient", study_id: int, event_id: int):
        """Initialize with study and event IDs."""
        super().__init__(client)
        self.study_id = study_id
        self.event_id = event_id
    
    @property
    def endpoint(self) -> str:
        return f"/api/grid/studies/{self.study_id}/events/{self.event_id}/details"
    
    @property
    def model_class(self):
        return StudyEventDetail


class StudyProcedureManager(BaseManager):
    """Manager for StudyProcedure resources."""
    
    def __init__(self, client: "BaseClient", study_id: int):
        """Initialize with study ID."""
        super().__init__(client)
        self.study_id = study_id
    
    @property
    def endpoint(self) -> str:
        return f"/api/grid/studies/{self.study_id}/procedures"
    
    @property
    def model_class(self):
        return StudyProcedure


class StudySubjectManager(BaseManager):
    """Manager for StudySubject resources."""
    
    def __init__(self, client: "BaseClient", study_id: int):
        """Initialize with study ID."""
        super().__init__(client)
        self.study_id = study_id
    
    @property
    def endpoint(self) -> str:
        return f"/api/grid/studies/{self.study_id}/subjects"
    
    @property
    def model_class(self):
        return StudySubject


class StudySubjectContactManager(BaseManager):
    """Manager for StudySubjectContact resources."""
    
    def __init__(self, client: "BaseClient", study_id: int, subject_id: int):
        """Initialize with study and subject IDs."""
        super().__init__(client)
        self.study_id = study_id
        self.subject_id = subject_id
    
    @property
    def endpoint(self) -> str:
        return f"/api/grid/studies/{self.study_id}/subjects/{self.subject_id}/contacts"
    
    @property
    def model_class(self):
        return StudySubjectContact


class GridManager:
    """Main manager for Grid API resources."""
    
    def __init__(self, client):
        """Initialize the Grid manager."""
        self.client = client
        
        # Initialize sub-managers
        self.studies = StudyManager(client)
        self.datatypes = DatatypeManager(client)
        self.subject_studies = SubjectStudyManager(client)
    
    def study(self, study_id: int):
        """Get a study-specific manager."""
        return StudyContextManager(self.client, study_id)


class StudyContextManager:
    """Context manager for study-specific operations."""
    
    def __init__(self, client: "BaseClient", study_id: int):
        """Initialize with client and study ID."""
        self.client = client
        self.study_id = study_id
        
        # Initialize study-specific managers
        self.events = StudyEventManager(client, study_id)
        self.procedures = StudyProcedureManager(client, study_id)
        self.subjects = StudySubjectManager(client, study_id)
    
    def event(self, event_id: int):
        """Get an event-specific manager."""
        return EventContextManager(self.client, self.study_id, event_id)
    
    def subject(self, subject_id: int):
        """Get a subject-specific manager."""
        return SubjectContextManager(self.client, self.study_id, subject_id)


class EventContextManager:
    """Context manager for event-specific operations."""
    
    def __init__(self, client: "BaseClient", study_id: int, event_id: int):
        """Initialize with client, study ID, and event ID."""
        self.client = client
        self.study_id = study_id
        self.event_id = event_id
        
        # Initialize event-specific managers
        self.details = StudyEventDetailManager(client, study_id, event_id)


class SubjectContextManager:
    """Context manager for subject-specific operations."""
    
    def __init__(self, client: "BaseClient", study_id: int, subject_id: int):
        """Initialize with client, study ID, and subject ID."""
        self.client = client
        self.study_id = study_id
        self.subject_id = subject_id
        
        # Initialize subject-specific managers
        self.contacts = StudySubjectContactManager(client, study_id, subject_id)
