from datetime import timedelta
from uuid import uuid4
from fastapi import Depends, HTTPException
from databaseStore.User.user_respository import UserRepository
from models.user import ReadHashedPassword, ReadUserModel, CreateUserModel
from services.userService.authHelper import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_password_hash, verify_password


class UserService:
    def __init__(self, user_repository: UserRepository =  Depends(UserRepository)):
        self.user_respository = user_repository


    def get_user_by_email(self, email: str) -> ReadUserModel:
        return self.user_respository.get_user_by_email(email)

    def get_user_by_id(self, id: uuid4 )-> ReadUserModel:
        return self.user_respository.get_user_by_id(id)    
    
    def get_hashed_password_by_email(self, email: str) -> ReadHashedPassword:
        return self.user_respository.get_hashed_password_by_email(email)
    
    def create_user(self, user: CreateUserModel) -> ReadUserModel:
        password  =  user.password
        hashed_password = get_password_hash(password)

        user_dict = user.dict()
        user_dict.pop("password")
        user_dict["hashed_password"] = hashed_password
        return self.user_respository.create_user(user_dict)
    

    def authenticate_user(self, email: str, password: str):
        authenticated_user = self._authicate_user(email, password)
        print(authenticated_user.email, "authenticated_user")
        if not authenticated_user:
            raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(authenticated_user.id)}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    def _authicate_user( self, email: str, password: str):
        user_with_hashed_password = self.get_hashed_password_by_email(email=email)
        print(user_with_hashed_password.hashed_password)
        if not user_with_hashed_password:
            return False
        if not verify_password(password, user_with_hashed_password.hashed_password):
            return False
        return user_with_hashed_password