from uuid import UUID

from fastapi import Depends

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from typing import Annotated

from models.aiOperations import AIOperations, AIOperationsReadModel

from database import get_db


class AIOperationsRepository:
    def __init__(self,  db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def  update_ai_operations(self, id: UUID, ai_operations : dict ) -> AIOperationsReadModel:
        self.db.query(AIOperations).filter(AIOperations.id == id).update( ai_operations, synchronize_session='evaluate')
        self.db.commit()

        ai_response = self.db.query(AIOperations).filter(AIOperations.id == id).first()
        return jsonable_encoder((AIOperationsReadModel.from_orm(ai_response).dict()))  

    def get_ai_operation(self) -> AIOperationsReadModel:
        response  =  self.db.query(AIOperations).where(AIOperations.deleted_at == None).first()  
        json_response  = jsonable_encoder((AIOperationsReadModel.from_orm(response).dict()))
        return json_response