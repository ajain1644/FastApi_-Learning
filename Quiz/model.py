from sqlalchemy import Integer, String, Boolean, ForeignKey, Column
from .database import Base

class Questions(Base):
    __tablename__ = "questions"
    id = Column(Integer,primary_key=True,index=True)
    question_text = Column(String,index=True)

class Choices(Base):
    __tablename__  = "choices"
    id = Column(Integer,primary_key=True,index=True)
    choice_text = Column(String,index=True)
    is_correct = Column(Boolean,default=False)
    question_id = Column(Integer,ForeignKey("questions.id"))