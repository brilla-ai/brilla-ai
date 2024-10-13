from typing import Annotated
from uuid import UUID


from fastapi import APIRouter, Depends, HTTPException

from models.aiOperations import AIOperationsUpdateModel

from services.aiOperationsService.ai_operations import AIOperationsService

from services.userService.oauth import get_current_user

from models.user import ReadUserModel, Role


ai_operations = APIRouter(tags=["ai_operations"], prefix="/operations")


@ai_operations.get("/operation")
def get_ai_operation( ai_operations_service: Annotated[AIOperationsService, Depends(AIOperationsService)], current_user: Annotated[ReadUserModel, Depends(get_current_user)]):
    if( current_user.role == Role.admin or  current_user.role == Role.moderator):
        return ai_operations_service.get_ai_operation()
    raise HTTPException(status_code=401, detail="Unauthorized")


@ai_operations.put("/operation/{id}")
def update_ai_operations(id: UUID, ai_operations : AIOperationsUpdateModel, ai_operations_service: Annotated[AIOperationsService, Depends(AIOperationsService)], current_user: Annotated[ReadUserModel, Depends(get_current_user)]):
    if( current_user.role == Role.admin or  current_user.role == Role.moderator):
        return ai_operations_service.update_ai_operations(id, ai_operations)
    raise HTTPException(status_code=401, detail="Unauthorized")
