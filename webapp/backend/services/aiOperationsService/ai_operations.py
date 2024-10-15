from typing import Annotated

from uuid import uuid4

from fastapi import Depends, status 

from core.reponse_model import BaseResponseModel

from helper.filter_none_values import  filter_none_values

from models.aiOperations import AIOperationsUpdateModel

from databaseStore.AIOperations.ai_operations import AIOperationsRepository
from .interface.IAi_operations import IAIOperationsService


class AIOperationsService(IAIOperationsService):
    def __init__(self, ai_operations_repository: Annotated[AIOperationsRepository, Depends(AIOperationsRepository)]):
        self.ai_opeations_repository = ai_operations_repository


    def update_ai_operations(self, id: uuid4, ai_operations : AIOperationsUpdateModel):
            ai_operations_dict  =  filter_none_values(ai_operations.model_dump())
            ai_opeartions_response  =   self.ai_opeations_repository.update_ai_operations(id, ai_operations_dict)
            
            return BaseResponseModel.create_response(ai_opeartions_response, "Ai operations updated successfully", status.HTTP_200_OK)


    def get_ai_operation(self):
            ai_opeartions_response  =   self.ai_opeations_repository.get_ai_operation()
            print( ai_opeartions_response )
            return BaseResponseModel.create_response(ai_opeartions_response, "Ai operations fetched successfully", status.HTTP_200_OK)
