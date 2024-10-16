from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


# Define the interface
class IAIOperationsService(ABC):
    
    @abstractmethod
    def update_ai_operations(self, id: UUID, ai_operations: Any) -> Any:
        """Update AI operations with the provided data."""
        pass

    @abstractmethod
    def get_ai_operation(self) -> Any:
        """Fetch AI operations."""
        pass

