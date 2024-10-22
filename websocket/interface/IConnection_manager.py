from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from fastapi import WebSocket


class IConnectionManager(ABC):
    
     
    @property
    @abstractmethod
    def active_connections(self) -> Dict[str, List[WebSocket]]:
        """Return the active connections grouped by their names."""
        pass

    @active_connections.setter
    @abstractmethod
    def active_connections(self, value: Dict[str, List[WebSocket]]) -> None:
        """Set the active connections."""
        pass

    @property
    @abstractmethod
    def client_connections(self) -> Dict[str, WebSocket]:
        """Return the individual client connections."""
        pass

    @client_connections.setter
    @abstractmethod
    def client_connections(self, value: Dict[str, WebSocket]) -> None:
        """Set the client connections."""
        pass


    @abstractmethod
    async def on_message_recieved_handler(self, websocket: WebSocket, message_handler: Any) -> None:
        """Handle incoming messages from a WebSocket client."""
        pass

    @abstractmethod
    def disconnect(self, websocket: WebSocket, group_name: Optional[str] = None) -> Optional[str]:
        """Disconnect a WebSocket connection."""
        pass

    @abstractmethod
    def get_connection_id(self, websocket: WebSocket) -> Optional[str]:
        """Get the connection ID for a given WebSocket."""
        pass

    @abstractmethod
    async def send_message_to_client(self, client_id: str, message: str) -> None:
        """Send a message to a specific WebSocket client."""
        pass

    @abstractmethod
    async def send_message_to_group(self, group_name: str, message: str) -> None:
        """Send a message to all WebSocket clients in a group."""
        pass