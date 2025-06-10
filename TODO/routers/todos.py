from TODO import models
from TODO.database import SessionLocal, engine, db_dependency
from fastapi import APIRouter, HTTPException, Depends, Path
from starlette import status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from .auth import get_current_user

router = APIRouter(
    tags=['Todos']
)
models.Base.metadata.create_all(bind=engine)

class TodoSchema(BaseModel):
    id: Optional[int] = Field(description="no need of id", default=None)
    title: str = Field(min_length=3)
    description: str = Field(min_length=3,max_length=100)
    priority: int = Field(gt=0,lt=6)
    complete: bool
    model_config = {
        "json_schema_extra":{
            "example":{
                "title": "new todo",
                "description": "new description",
                "priority": 1,
                "complete": False
            }
        }
    }

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

user_dependency = Annotated[dict,Depends(get_current_user)]


@router.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(user: user_dependency,todo: TodoSchema, db: db_dependency):
    db_todo = models.TODO(**todo.model_dump(), owner_id=user.get('id'))
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.get("/todos",status_code=status.HTTP_200_OK)
def get_Todos(db: db_dependency):
    result = db.query(models.TODO).all()
    if not result:
        raise HTTPException(status_code=404, detail="Todo not found")
    return result

@router.get("/todos/{todo_id}",status_code=status.HTTP_200_OK)
def get_Todo_By_Id(db: db_dependency, todo_id: int = Path(gt=0)):
    result = db.query(models.TODO).filter(models.TODO.id == todo_id).first()
    if not result:
        raise HTTPException(404, detail='no todo with such id')
    return result

@router.put("/todos/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
def update_todo(todo: TodoSchema,todo_id: int,db: db_dependency):
    result = db.query(models.TODO).filter(models.TODO.id == todo_id).first()
    if result is None:
        raise HTTPException(404,detail="todo not found")
    result.title = todo.title
    result.description = todo.description
    result.priority = todo.priority
    result.complete = todo.complete
    db.add(result)
    db.commit()
    
@router.delete("/todos/{todo_id}")
def delete_todo(db :db_dependency,todo_id: int=Path(gt=0)):
    result = db.query(models.TODO).filter(models.TODO.id==todo_id)
    if result is None:
        raise HTTPException(404,detail="todo not found!")
    db.query(models.TODO).filter(models.TODO.id==todo_id).delete() 
    db.commit()
