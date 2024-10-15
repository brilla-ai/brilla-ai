


from typing import  Dict, List
import uuid

from fastapi import Depends, WebSocket, WebSocketDisconnect

from .interface.IConnection_manager import IConnectionManager

from .websocket_command_handler import CommandHandler

import re

class ConnectionManager( IConnectionManager):
    def __init__(self) -> None:
        self.active_connections: Dict[str, List[WebSocket]] = {}  # Group-based connections
        self.client_connections: Dict[str, WebSocket] = {}  # Individual client connections


    @property
    def active_connections(self) -> Dict[str, List[WebSocket]]:
        return self._active_connections

    @active_connections.setter
    def active_connections(self, value: Dict[str, List[WebSocket]]) -> None:
        self._active_connections = value

    @property
    def client_connections(self) -> Dict[str, WebSocket]:
        return self._client_connections

    @client_connections.setter
    def client_connections(self, value: Dict[str, WebSocket]) -> None:
        self._client_connections = value

    async def connect(self, websocket: WebSocket):

        
        try:
            await websocket.accept()  # Accept the incoming WebSocket connection

            #  random concetion_id  
            connection_id = str(uuid.uuid4())  # Generate a unique connection ID
            self.client_connections[connection_id] = websocket
            # self.client_connections[client_id] = websocket
            print(f"Current client connections: {self.client_connections}")
            await websocket.send_json({"type": 1, "target": "handshake", "connection_id": connection_id, "version": "1.0.0", "protocol": "json"})
    
        except WebSocketDisconnect:
            connection_id = self.disconnect(self, websocket)
            print(f"Client {connection_id} disconnected")


    async  def  on_message_recieved_handler(self, websocket: WebSocket, message_handler: CommandHandler):
         while True:
                # Wait for the client to send a message
                data = await websocket.receive_text()
               

                # Process the received message
                command_response  = await message_handler.remote_command_handler(data)
                print(command_response, "error message ")
                if('error' in command_response):
                    await websocket.send_json({"type": 1, "target": "error_message", "error": command_response, "version": "1.0.0", "protocol": "json"})

                # Send a response back to the client
                # await websocket.send_text(response)

    def disconnect(self, websocket: WebSocket, client_id: str, group_name: str = None):
        if group_name and group_name in self.active_connections:
            self.active_connections[group_name].remove(websocket)
            if not self.active_connections[group_name]:
                del self.active_connections[group_name]
        if client_id in self.client_connections:
            del self.client_connections[client_id]
        
    
    def disconnect(self, websocket: WebSocket, group_name : str  = None):
        
        
        if( group_name and group_name in self.active_connections):
            self.active_connections[group_name].remove(websocket)

            if not self.active_connections[group_name]:
                del self.active_connections[group_name]

        connection_id = self.get_connection_id(websocket)
        if connection_id:
            del self.client_connections[connection_id] 
        return connection_id    


    def get_connection_id(self, websocket: WebSocket) -> str:
        for connection_id, conn in self.client_connections.items():
            if conn == websocket:
                return connection_id
        return None

                  

    async def send_message_to_client(self, client_id: str, message: str):
        if client_id in self.client_connections:
            websocket = self.client_connections[client_id]
            await websocket.send_text(message)

    async def send_message_to_group(self, group_name: str, message: str, type: str = "json"):
        print("Sending message")
        pattern = r"^send_"
        connection_type = ""

        if re.match(pattern, type):
            connection_type = type
        else:
            connection_type = "send_" + type

        if group_name in self.active_connections:
            print(self.active_connections[group_name], "name of the group " + group_name)
            for connection in self.active_connections[group_name]:
                print(connection, "connection")
                try:
                    method = getattr(connection, connection_type, None)
                    if not (method and callable(method)):
                        await connection.send_text("Connection type not supported")
                    await method(message)
                except Exception as e:
                    print(f"Error sending message to connection: {connection}, error: {e}")
        

    