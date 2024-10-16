


from typing import Annotated
from uuid import uuid4
from fastapi import Depends
from sqlalchemy.orm import Session
from models.user import InviteUser, UpdateInviteUserModel
from database import get_db


class InviteRepository:
    def __init__(self,  db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def get_invite_by_id(self, id: uuid4):
        return self.db.query(InviteUser).filter(InviteUser.id == id).first()
    
    def get_invite_by_code(self, code: str):
        return self.db.query(InviteUser).filter(InviteUser.invite_code == code).first()
    
    def create_invite(self, invite: InviteUser):
        invite = InviteUser(**invite)
        self.db.add(invite)
        self.db.commit()
        self.db.refresh(invite)
        return invite
    
    def update_invite(self, invite: UpdateInviteUserModel):
        invite_user = self.db.query(InviteUser).filter(InviteUser.id == invite["id"]).first()
        if( not invite_user ):
            return None
        self.db.query(InviteUser).filter(InviteUser.id == invite["id"]).update( invite, synchronize_session='evaluate')
        self.db.commit()
        self.db.refresh(invite_user)
        return invite