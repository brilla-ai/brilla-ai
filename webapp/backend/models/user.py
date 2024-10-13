
from typing import Optional
from sqlalchemy import Column, String, Boolean, DateTime,  Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.dialects.postgresql  import UUID 
from sqlalchemy.orm import relationship
from database import Base
from uuid import uuid4
from uuid import UUID as type_uuid
from pydantic import BaseModel
from datetime import datetime, timedelta
from  enum import Enum 



#  Enum 

class Role(str, Enum):
    admin = "admin"
    user = "user"
    moderator = "moderator"

#  Database models

class DefaultData:
    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, index=True)
    created_at = Column(DateTime , default=datetime.utcnow())
    deleted_at = Column(DateTime, default=None, nullable=True)
    updated_at = Column(DateTime , default=datetime.utcnow())


class User(Base, DefaultData):
    __tablename__ = "users"
    email = Column(String, unique=True, index=True)
    first_name = Column(String(2004))
    last_name = Column(String(2004))
    hashed_password = Column(String(2004))
    is_active = Column(Boolean, default=True)
    role = Column(SQLAlchemyEnum(Role), default=Role.user)
    invite_id  =   Column(UUID(as_uuid=True),  ForeignKey("invite_users.id", ondelete="CASCADE"), nullable=True)
    invite = relationship("InviteUser", back_populates="user") 

class InviteUser(Base, DefaultData):
    __tablename__ = "invite_users"
    email = Column(String(2004), unique=True, index=True)
    is_active = Column(Boolean, default=True)
    role = Column(SQLAlchemyEnum(Role), default=Role.user)
    full_name = Column(String(2004))
    expires_at = Column(DateTime, default=datetime.utcnow() + timedelta(days=2))
    user = relationship("User", back_populates="invite")
    invite_code = Column(String(2004), unique=True, index=True)
  

#  Pydantic models
class ReadUserModel(BaseModel):
    id: type_uuid
    email: str
    is_active: bool
    role: Role
    first_name:  str
    last_name:  str

    class Config: 
        from_attributes = True

class ReadHashedPassword(ReadUserModel):
    hashed_password: str

class CreateUserModel(BaseModel):
    email: str
    password: str
    role: Role = Role.user
    first_name: str 
    last_name: str

class UpdateUserModel(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Role = Role.user
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    class Config:
        from_attributes = True



class BaseInviteUserModel(BaseModel):
    email: str
    full_name: str
    role: str
class CreateInviteUserModel(BaseInviteUserModel):
    email: str
    full_name: str
    role: str

class UpdateInviteUserModel(BaseModel):
    id: type_uuid
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ReadInviteUserModel(BaseInviteUserModel):
    id: type_uuid
    is_active: bool
    expires_at: datetime


class ReadInviteUserWithCodeModel(ReadInviteUserModel):
    invite_code: str




class AcceptInviteModel(BaseModel):
    invite_code: str
    password: str

class  CreateAcceptInviteModel(ReadInviteUserModel,AcceptInviteModel ):
      pass

class LoginUserModel(BaseModel):
    email: str
    password: str

class TokenData(BaseModel):
    user_id: str

class Token(BaseModel):
    access_token: str
    token_type: str