from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models.user import AcceptInviteModel, CreateInviteUserModel, CreateUserModel, ReadUserModel, Token
from services.userService.oauth import  get_current_active_user
from services.userService.user import UserService
from services.userService.invite_user import InviteUserService


user_router = APIRouter(tags=["user"], prefix="/users")
# Login endpoint
@user_router.post("/token", response_model=Token)
async def login_for_access_token(user_service : Annotated[UserService , Depends(UserService)] , form_data: OAuth2PasswordRequestForm = Depends()):
    token = user_service.authenticate_user( form_data.username, form_data.password)
    return token 

# Me endpoint
@user_router.get("/me", response_model=ReadUserModel)
async def read_users_me(current_user: ReadUserModel = Depends(get_current_active_user)):
    return current_user

@user_router.post("/create")
async def create_user(create_user: CreateUserModel , user_service : Annotated[UserService , Depends(UserService)]):
    # if( current_user.role):
        user = user_service.create_user(create_user)
        return {"message": "User created", "user": user}
    # else:
    #     raise HTTPException(status_code=401, detail="Unauthorized")



@user_router.post("/invite")
async def create_invite(invite_user: CreateInviteUserModel , user_service : Annotated[InviteUserService , Depends(InviteUserService)], current_user: ReadUserModel = Depends(get_current_active_user)):
    if( current_user.role):
        invite_data  = user_service.create_invite(invite_user)

        return invite_data
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    

@user_router.post("/invite/accept")
async def accept_invite(accept_invite: AcceptInviteModel, invite_service : Annotated[InviteUserService , Depends(InviteUserService)]):
    invite = invite_service.get_invite_by_code(accept_invite.invite_code)
    if( invite ):
        invite_data =  invite.__dict__
        invite_data["password"] = accept_invite.password
        create_user  = invite_service.create_user_from_invite(invite)
        return create_user
        
    elif ( invite == None ):
        raise HTTPException(status_code=404, detail="Invite not found")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")