from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from ..database import db_dependency
from typing import Annotated
from starlette import status
from .. import models
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')


router = APIRouter(
    tags=['User']
)

class UserSchema(BaseModel):
    email: str
    username: str = Field(min_length=3)
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    password: str
    is_active: bool 
    role: str = Field(default="user")
    
    model_config={"json_schema_extra":{
        "example":{
            "email":"xyz@gmail.com",
            "username":"abcd",
            "first_name":"aman",
            "last_name":"jain",
            "password":"hdoufhofjfkisd",
            "is_active":True,
        }
    }}


@router.post("/user",status_code=status.HTTP_201_CREATED)

def create_User(db:db_dependency,user: UserSchema):
    db_user = models.USERS(
        email = user.email,
        username = user.username,
        first_name = user.first_name,
        last_name = user.last_name,
        hashed_password = bcrypt_context.hash(user.password),
        is_active = user.is_active,
        role = user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users",status_code=status.HTTP_200_OK)
def get_Users(db: db_dependency):
    result = db.query(models.USERS).all()
    if result is None:
        HTTPException(404,detail="users not found!")
    return result

