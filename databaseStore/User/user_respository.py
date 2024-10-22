from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends
from database import get_db
from models.user import User
from uuid import uuid4


class UserRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):   
        self.db  = db

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, id: uuid4 ):
        return self.db.query(User).filter(User.id == id).first()
    
    def create_user(self, user: User):
        user  = User(**user)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user.__dict__
    
    def get_hashed_password_by_email(self, email: str):
        password =  self.db.query(User).filter(User.email == email).first()
        if not password:
            return None
        return password
    