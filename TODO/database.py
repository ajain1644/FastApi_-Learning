from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Depends
from typing import Annotated


DATABASEURL = 'postgresql://aman:aman123@localhost:5432/fastapi_db'

engine = create_engine(DATABASEURL)

SessionLocal = sessionmaker(bind=engine,expire_on_commit=False,autoflush=False)

Base = declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]