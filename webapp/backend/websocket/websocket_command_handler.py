
import json


from .base_comand_executor import BaseCommandExecutor




class CommandHandler:
    def __init__(self, command_executor: BaseCommandExecutor ) -> None:
        self.command_executor = command_executor 

    async def remote_command_handler(self,data: dict): 
        try:
            print( data)
            command = json.loads(data)  # Parse the incoming JSON message

            # Check for required fields
            command_type = command.get("type")
            target_method = command.get("target")
            arguments = command.get("arguments", [])

            # Dispatch method based on target
            if command_type == 1:  # Assuming type 1 means invoking a method
                print("method dispatched")
                result = await self.command_executor.execute(target_method, *arguments)
                return json.dumps({"result": result})
            else:
                return json.dumps({"error": "Unsupported command type"})

        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON format"})
        except Exception as e:
            return json.dumps({"error": str(e)})  
        

    # async def method_dispatcher(self, target: str, arguments: list):
    #     # Check if the target method exists and is callable
    #     from  core.command_handler.websocket_command_handler import WebSocketCommands
    #     from  core.command_handler.websocket_command_handler import get_connection_manager, LiveVideoService, AIOperationsService
    #     live_service : LiveVideoService = Depends(LiveVideoService)
    #     ai_service : AIOperationsService = Depends(AIOperationsService)
    #     connection_manager =  Depends(get_connection_manager())
    #     commands  = WebSocketCommands( live_video_service=live_service, ai_operations_service=ai_service, websocket_connection_manager=connection_manager)
    #     method = getattr(commands, target, None)
    
    #     if method and callable(method):
    #         print("calling method")
    #         try:
    #             return await method(*arguments)  # Call the method with the arguments
    #         except Exception as e:
    #             return {"error": str(e)}
    #     else:
    #         return {"error": f"No method found for target: {target}"}


    