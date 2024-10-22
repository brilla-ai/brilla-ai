from datetime import datetime, timedelta
from typing import Optional, Annotated
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from models.user import ReadUserModel, TokenData
from services.userService.user import UserService

#  TODO: Put in a separate constant class file
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Set up OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


# Get current user function
async def get_current_user(user_service : Annotated[UserService , Depends(UserService)], token: str = Depends(dependency=oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    user = user_service.get_user_by_id(token_data.user_id)
    if user is None:
        raise credentials_exception
    return user

# Get current active user function
async def get_current_active_user(current_user: ReadUserModel = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user