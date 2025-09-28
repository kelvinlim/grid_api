"""
Image API resource manager.
"""

from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from datetime import datetime
from ..models.image import (
    Acquisition,
    Action,
    ActionType,
    Destination,
    RawDataIn,
    ScannerType,
)
from .base import BaseManager

if TYPE_CHECKING:
    from ..client import BaseClient


class AcquisitionManager(BaseManager):
    """Manager for Acquisition resources."""
    
    @property
    def endpoint(self) -> str:
        return "/api/image/acquisition"
    
    @property
    def model_class(self):
        return Acquisition


class ActionManager(BaseManager):
    """Manager for Action resources."""
    
    @property
    def endpoint(self) -> str:
        return "/api/image/action"
    
    @property
    def model_class(self):
        return Action
    
    def list(
        self,
        finishtime: Optional[datetime] = None,
        starttime: Optional[datetime] = None,
        status: Optional[str] = None,
        **kwargs
    ) -> Union[List[Action], Dict[str, Any]]:
        """List actions with filtering."""
        return super().list(
            finishtime=finishtime,
            starttime=starttime,
            status=status,
            **kwargs
        )


class ActionTypeManager(BaseManager):
    """Manager for ActionType resources."""
    
    @property
    def endpoint(self) -> str:
        return "/api/image/actiontype"
    
    @property
    def model_class(self):
        return ActionType
    
    def list(
        self,
        description: Optional[str] = None,
        label: Optional[str] = None,
        **kwargs
    ) -> Union[List[ActionType], Dict[str, Any]]:
        """List action types with filtering."""
        return super().list(
            description=description,
            label=label,
            **kwargs
        )


class DestinationManager(BaseManager):
    """Manager for Destination resources."""
    
    @property
    def endpoint(self) -> str:
        return "/api/image/destination"
    
    @property
    def model_class(self):
        return Destination
    
    def list(
        self,
        study: Optional[int] = None,
        **kwargs
    ) -> Union[List[Destination], Dict[str, Any]]:
        """List destinations with filtering."""
        return super().list(
            study=study,
            **kwargs
        )


class RawDataInManager(BaseManager):
    """Manager for RawDataIn resources."""
    
    @property
    def endpoint(self) -> str:
        return "/api/image/rawdatain"
    
    @property
    def model_class(self):
        return RawDataIn
    
    def list(
        self,
        accession: Optional[str] = None,
        grid_match: Optional[bool] = None,
        receivetime: Optional[datetime] = None,
        **kwargs
    ) -> Union[List[RawDataIn], Dict[str, Any]]:
        """List raw data inputs with filtering."""
        return super().list(
            accession=accession,
            grid_match=grid_match,
            receivetime=receivetime,
            **kwargs
        )


class ScannerTypeManager(BaseManager):
    """Manager for ScannerType resources."""
    
    @property
    def endpoint(self) -> str:
        return "/api/image/scannertype"
    
    @property
    def model_class(self):
        return ScannerType
    
    def list(
        self,
        cmrr_name: Optional[str] = None,
        description: Optional[str] = None,
        label: Optional[str] = None,
        **kwargs
    ) -> Union[List[ScannerType], Dict[str, Any]]:
        """List scanner types with filtering."""
        return super().list(
            cmrr_name=cmrr_name,
            description=description,
            label=label,
            **kwargs
        )


class ImageManager:
    """Main manager for Image API resources."""
    
    def __init__(self, client):
        """Initialize the Image manager."""
        self.client = client
        
        # Initialize sub-managers
        self.acquisitions = AcquisitionManager(client)
        self.actions = ActionManager(client)
        self.action_types = ActionTypeManager(client)
        self.destinations = DestinationManager(client)
        self.raw_data = RawDataInManager(client)
        self.scanner_types = ScannerTypeManager(client)
