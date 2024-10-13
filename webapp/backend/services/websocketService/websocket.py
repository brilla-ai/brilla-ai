


from typing import Annotated

from fastapi import Depends, WebSocket

from core.websocket_connection_manager import ConnectionManager, get_connection_manager


class WebSocketService:
    def __init__(self, connection_manager: Annotated[ConnectionManager, Depends(get_connection_manager)]):
        self.connection_manager = connection_manager

    async def send_message_to_client(self, client_id: str, message: str):
        await self.connection_manager.send_message_to_client(client_id, message)

    async def send_message_to_group(self, group_name: str, message: str):
        await self.connection_manager.send_message_to_group(group_name, message)

    async def on_message_recieved_handler(self, websocket: WebSocket, message_handler):
        await self.connection_manager.on_message_recieved_handler(websocket, message_handler)

    async def connect(self, websocket: WebSocket):
        await self.connection_manager.connect(websocket)

    async def disconnect(self, websocket: WebSocket, client_id: str, group_name: str = None):
        await self.connection_manager.disconnect(websocket, client_id, group_name)
    
    async  def add_client_to_group(self, client_id: str, group_name: str):
        await self.connection_manager.connect(self.connection_manager.client_connections[client_id], client_id, group_name)