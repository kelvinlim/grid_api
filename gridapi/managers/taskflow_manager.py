"""
Taskflow API resource manager.
"""

from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from .base import BaseManager

if TYPE_CHECKING:
    from ..client import BaseClient


class MeasureManager(BaseManager):
    """Manager for Measure resources."""
    
    def __init__(self, client: "BaseClient", study_id: int):
        """Initialize with study ID."""
        super().__init__(client)
        self.study_id = study_id
    
    @property
    def endpoint(self) -> str:
        return f"/api/taskflow/study/{self.study_id}/measures"
    
    @property
    def model_class(self):
        # Note: Measure model not defined in the OpenAPI spec
        # This would need to be added based on actual API response
        return dict


class ParticipantManager(BaseManager):
    """Manager for Participant resources."""
    
    def __init__(self, client: "BaseClient", study_id: int):
        """Initialize with study ID."""
        super().__init__(client)
        self.study_id = study_id
    
    @property
    def endpoint(self) -> str:
        return f"/api/taskflow/study/{self.study_id}/participants"
    
    @property
    def model_class(self):
        # Note: Participant model not defined in the OpenAPI spec
        # This would need to be added based on actual API response
        return dict


class ParticipantMeasureManager(BaseManager):
    """Manager for Participant Measure resources."""
    
    def __init__(self, client: "BaseClient", study_id: int, participant_id: int):
        """Initialize with study and participant IDs."""
        super().__init__(client)
        self.study_id = study_id
        self.participant_id = participant_id
    
    @property
    def endpoint(self) -> str:
        return f"/api/taskflow/study/{self.study_id}/participants/{self.participant_id}/measures"
    
    @property
    def model_class(self):
        # Note: ParticipantMeasure model not defined in the OpenAPI spec
        # This would need to be added based on actual API response
        return dict


class TaskflowManager:
    """Main manager for Taskflow API resources."""
    
    def __init__(self, client):
        """Initialize the Taskflow manager."""
        self.client = client
    
    def study(self, study_id: int):
        """Get a study-specific taskflow manager."""
        return StudyTaskflowManager(self.client, study_id)


class StudyTaskflowManager:
    """Context manager for study-specific taskflow operations."""
    
    def __init__(self, client: "BaseClient", study_id: int):
        """Initialize with client and study ID."""
        self.client = client
        self.study_id = study_id
        
        # Initialize study-specific managers
        self.measures = MeasureManager(client, study_id)
        self.participants = ParticipantManager(client, study_id)
    
    def participant(self, participant_id: int):
        """Get a participant-specific manager."""
        return ParticipantContextManager(self.client, self.study_id, participant_id)


class ParticipantContextManager:
    """Context manager for participant-specific operations."""
    
    def __init__(self, client: "BaseClient", study_id: int, participant_id: int):
        """Initialize with client, study ID, and participant ID."""
        self.client = client
        self.study_id = study_id
        self.participant_id = participant_id
        
        # Initialize participant-specific managers
        self.measures = ParticipantMeasureManager(client, study_id, participant_id)
