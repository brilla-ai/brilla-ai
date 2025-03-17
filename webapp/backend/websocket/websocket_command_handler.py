
import json


from .base_command_executor import BaseCommandExecutor




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
        


    