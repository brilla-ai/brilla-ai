from fastapi import Depends

from ..factory import get_command_executor

from websocket.websocket_command_handler import CommandHandler

from websocket.base_comand_executor import BaseCommandExecutor


def get_command_handler(command_executor: BaseCommandExecutor = Depends(get_command_executor)) -> CommandHandler:
    return CommandHandler(command_executor)