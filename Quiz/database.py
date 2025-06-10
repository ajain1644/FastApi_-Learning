from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASEURL = "postgresql://aman:aman123@localhost:5432/fastapi_db"

engine = create_engine(DATABASEURL)

SessionLocal = sessionmaker(expire_on_commit=False,bind=engine,autoflush=False)

Base = declarative_base()