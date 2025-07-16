
from abc import ABC, abstractmethod

class BaseCommandExecutor(ABC):
    
    @abstractmethod
    async def execute(self, command_name: str, *args, **kwargs):
        pass
