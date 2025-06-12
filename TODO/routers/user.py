from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import db_dependency
from typing import Annotated
from starlette import status
from models import USERS
from .security import bcrypt_context
from .auth import get_current_user

user_dependency = Annotated[dict,Depends(get_current_user)]
class changePassword(BaseModel):
    oldpassword: str
    newpassword: str

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
    phone_Num: str = Field(min_length=10,max_length=10)
    
    model_config={"json_schema_extra":{
        "example":{
            "email":"xyz@gmail.com",
            "username":"abcd",
            "first_name":"aman",
            "last_name":"jain",
            "password":"hdoufhofjfkisd",
            "is_active":True,
            "phone_Num":'4564564548'
        }
    }}


# @router.post("/user",status_code=status.HTTP_201_CREATED)

# def create_User(db:db_dependency,user: UserSchema):
#     db_user = USERS(
#         email = user.email,
#         username = user.username,
#         first_name = user.first_name,
#         last_name = user.last_name,
#         hashed_password = bcrypt_context.hash(user.password),
#         is_active = user.is_active,
#         role = user.role
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

@router.get("/user",status_code=status.HTTP_200_OK)
def get_User(user:user_dependency,db: db_dependency):
    result = db.query(USERS).filter_by(id=user.get('id')).one()
    if result is None:
        HTTPException(404,detail="users not found!")
    return result

@router.put("/users/chnpwd",status_code=status.HTTP_204_NO_CONTENT)
def change_password(user: user_dependency,db: db_dependency,pwdupdate: changePassword):
    usr_db = db.query(USERS).filter_by(id=user.get('id')).one() 
    if usr_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    if not bcrypt_context.verify(pwdupdate.oldpassword,usr_db.hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="incorrect password!")
    usr_db.hashed_password = bcrypt_context.hash(pwdupdate.newpassword)
    db.add(usr_db)
    db.commit()

@router.put("/users/updtnumber",status_code=status.HTTP_204_NO_CONTENT)
def updateNUm(user:user_dependency,db:db_dependency,number: str):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="please login!!")
    if len(number)!=10:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Inalid number")
    user_db = db.query(USERS).filter_by(id=user.get('id')).one()
    user_db.phone_Num = number;
    db.add(user_db)
    db.commit()
    return None