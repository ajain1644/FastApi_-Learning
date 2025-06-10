from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from starlette import status
from typing import List, Annotated
from .database import engine, SessionLocal
from . import model
from sqlalchemy.orm import Session

app = FastAPI()
model.Base.metadata.create_all(bind=engine)

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choice: List[ChoiceBase]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

@app.post("/questions",status_code=status.HTTP_201_CREATED)
async def create_question(question:QuestionBase,db:db_dependency):
    db_question = model.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choi in question.choice:
        db_choice = model.Choices(choice_text=choi.choice_text,is_correct=choi.is_correct,question_id = db_question.id)
        db.add(db_choice)
    db.commit()

@app.get("/questions/{question_id}")
async def required_question(question_id: int,db:db_dependency):
    result = db.query(model.Questions).filter(model.Questions.id == question_id).first()
    if not result:
        raise HTTPException(status_code=404,details='Question not found!')
    return result
