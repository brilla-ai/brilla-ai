from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class ILiveVideoService(ABC):
    
    @abstractmethod
    def create_live_video(self, live_video: Any, user_id: UUID) -> Any:
        """Create a new live video."""
        pass

    @abstractmethod
    def update_live_video(self, id: UUID, live_video: Any, user_id: UUID) -> Any:
        """Update an existing live video."""
        pass

    @abstractmethod
    def get_live_video_by_id(self, id: UUID) -> Any:
        """Fetch a live video by its ID."""
        pass

    @abstractmethod
    def get_all_live_video(self) -> Any:
        """Fetch all live videos."""
        pass

    @abstractmethod
    def delete_live_video(self, id: UUID, user_id: UUID) -> Any:
        """Delete a live video by its ID."""
        pass

    @abstractmethod
    def stop_live_video_update(self, id: UUID, user_id: UUID, stop_status: Any) -> Any:
        """Stop updates for a live video."""
        pass
    @abstractmethod
    def   update_live_video_status(self, id: UUID, status: Any) -> Any:
        """Update the status of a live video."""
        pass