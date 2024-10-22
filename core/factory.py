# core/command_handler/factory.py

from fastapi import Depends
from core.command_handler.websocket_command_handler import WebSocketCommands
from services.aiOperationsService.ai_operations import AIOperationsService
from services.videoService.video_service import LiveVideoService
from .websocket_connection_manager import get_connection_manager
from websocket.base_comand_executor import BaseCommandExecutor

def get_command_executor(
    live_video_service = Depends(LiveVideoService),
    ai_operations_service = Depends(AIOperationsService),
    connection_manager = Depends(get_connection_manager),
) -> BaseCommandExecutor:
    return WebSocketCommands(live_video_service, ai_operations_service, connection_manager)
