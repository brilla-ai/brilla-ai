from datetime import datetime
from typing import Annotated, Optional
from fastapi import Depends
from models.user import AcceptInviteModel, CreateAcceptInviteModel, CreateInviteUserModel, ReadInviteUserModel, ReadUserModel, Role, User
from databaseStore.User.invite_repository import InviteRepository
from helper.generate_invite_code import generate_invite_code
from databaseStore.User.user_respository import UserRepository
from .authHelper import get_password_hash


class InviteUserService:

    def __init__(self, invite_repository: Annotated[InviteRepository, Depends(InviteRepository)], user_respository: Annotated[UserRepository, Depends(UserRepository)] ) -> None:
        self.invite_repository = invite_repository
        self.user_repository = user_respository
    def create_invite(self, invite_user: CreateInviteUserModel) -> dict:
        if( invite_user.role not in Role._value2member_map_):
            return {"message": "Invalid role", "data": None}
        
        invite_data = invite_user.dict()
        invite_data["invite_code"] = generate_invite_code()
        invite_user = self.invite_repository.create_invite(invite_data)
        invite_user = ReadInviteUserModel(**invite_user.__dict__)
        return {"message": "User invite sent", "data": invite_user}
    

    def get_invite_by_code(self, invite_code: str) -> ReadInviteUserModel:
        return self.invite_repository.get_invite_by_code(invite_code)

    def create_user_from_invite(self, invite: CreateAcceptInviteModel) -> Optional[ReadUserModel | dict ]:
        
        first_name , last_name = invite.full_name.split(" ")
        if(invite.password == "") or invite.expires_at < datetime.utcnow() or invite.is_active == False:
            return None
        hashed_password = get_password_hash(invite.password)

        if invite.role not in Role._value2member_map_:
            print(invite.role, "invite role from create_user_from_invite")
            return {"message": "Invalid role", "data": None}

        user_data  = {
            "email": invite.email,
            "first_name": first_name,
            "last_name": last_name,
            "role": invite.role,
            "hashed_password": hashed_password,
            "invite_id": invite.id
        }
        user_exist = self.user_repository.get_user_by_email(invite.email)

        if( user_exist ):
            return {"message": "User already exist", "data": None}
        
        user = self.user_repository.create_user(user_data)

        invite_data =   self.deactive_invite(invite.invite_code)
        if( invite_data ):
            return {"message": "User created", "data": ReadUserModel(**user).__dict__}
        return {"message": "User already exist", "data": ReadUserModel(**user).__dict__}
    
    def  deactive_invite(self, invite_code: str):
        invite = self.invite_repository.get_invite_by_code(invite_code)
        if( invite and invite.is_active ):
            invite_data  = {
                            "id": invite.id,
                            "is_active": False,
                            "expires_at": datetime.utcnow()}
            self.invite_repository.update_invite(invite_data)
            return True
        else:
            return False