# core/command_handler/base_command_executor.py

from abc import ABC, abstractmethod

class BaseCommandExecutor(ABC):
    
    @abstractmethod
    async def execute(self, command_name: str, *args, **kwargs):
        pass
