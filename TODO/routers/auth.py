from fastapi import APIRouter, Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from pydantic import BaseModel
from starlette import status
from database import db_dependency
import models
from .security import bcrypt_context
from jose import jwt, JWTError
from datetime import timedelta,datetime,timezone

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

SECRET_KEY = 'a55d3fd001587bebfadd66518b2e2a66caa306499ff3d70bd5d461d0127c3ce4'
ALGORITHM = 'HS256'

class Token(BaseModel):
    access_token: str
    token_type: str

def authenticateUser(db,username: str,password: str):
    user = db.query(models.USERS).filter(models.USERS.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user

def create_access_token(username: str,user_id: int,role: str,expire_delta: timedelta):
    encode = {'sub':username,'id':user_id,'role':role}
    expires = datetime.now(timezone.utc) + expire_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,ALGORITHM)

def get_current_user(token: Annotated[OAuth2PasswordBearer,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,ALGORITHM)
        username = payload.get('sub')
        user_id = payload.get('id')
        user_role = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate user!")
        return {'username':username,'id':user_id,'role':user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate user!")


@router.post("/token",response_model=Token,status_code=status.HTTP_200_OK)
async def login_for_access_token(
    db: db_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticateUser(db,username=form_data.username,password=form_data.password)
    if not user:
        raise HTTPException(401,"Username or Password is incorrect!")
    token = create_access_token(user.username,user.id,user.role,timedelta(minutes=20))

    return {'access_token': token,'token_type':'bearer'}