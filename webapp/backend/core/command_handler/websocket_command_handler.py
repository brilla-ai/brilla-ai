from services.aiOperationsService.interface.IAi_operations import IAIOperationsService
from services.videoService.interface.ILive_video_service import ILiveVideoService
from websocket.interface.IConnection_manager import IConnectionManager


class WebSocketCommands:

    def __init__(self, live_video_service: ILiveVideoService, ai_operations_service: IAIOperationsService, websocket_connection_manager:IConnectionManager ):
        self.live_video_service = live_video_service
        self.ai_operations_service = ai_operations_service
        self.websocket_connection_manager = websocket_connection_manager

        #  custom method handler to be invoked by the client

    async def execute(self, command_name: str, *args, **kwargs):
        method = getattr(self, command_name, None)
        if method and callable(method):
            return await method(*args, **kwargs)
        return {"error": f"No method found for command: {command_name}"}
    
    async  def  get_all_video(self):
        
        response  = self.live_video_service.get_all_live_video()
        await self.websocket_connection_manager.send_message_to_group("live_video", response)
    
    async  def  get_ai_operations(self):
        
        response  =   self.ai_operations_service.get_ai_operation()
        print(response)
        await self.websocket_connection_manager.send_message_to_group("ai_operations", response)

    #  System method handler 
    async  def add_to_group(self, client_id: str, group_name: str):
        if client_id in self.websocket_connection_manager.client_connections:
            websocket = self.websocket_connection_manager.client_connections[client_id]

            if group_name:
                    # Check if the group already exists in active connections
                    if group_name not in self.websocket_connection_manager.active_connections:
                        print("Group name not in active connections:", group_name)
                        self.websocket_connection_manager.active_connections[group_name] = []  # Initialize a new list for this group
                    
                    # Add the new WebSocket connection to the group
                    if( websocket not in self.websocket_connection_manager.active_connections[group_name]):
                        self.websocket_connection_manager.active_connections[group_name].append(websocket)
                        print(f"Added WebSocket to group '{group_name}', total connections now: {len(self.websocket_connection_manager.active_connections[group_name])}")
                        print("Current active connections:", self.websocket_connection_manager.active_connections) 
                        await  websocket.send_json({"type": 1, "target": "handshake", "success": "WebSocket added to group", "version": "1.0.0", "protocol": "json"})
                          
                    else: 
                        print("websocket already in group")
                        await websocket.send_json({"type": 1, "target": "error_message", "error": "WebSocket already in group", "version": "1.0.0", "protocol": "json"})
        else:
            print("Client ID not found in client_connections")


    async def remove_from_group(self, client_id: str, group_name: str):
        if client_id in self.websocket_connection_manager.client_connections:
            websocket = self.websocket_connection_manager.client_connections[client_id]
            if group_name in self.websocket_connection_manager.active_connections:
                self.websocket_connection_manager.active_connections[group_name].remove(websocket)
                if not self.websocket_connection_manager.active_connections[group_name]:
                    del self.websocket_connection_manager.active_connections[group_name]
            print("Current active connections:", self.websocket_connection_manager.active_connections) 
    
        

