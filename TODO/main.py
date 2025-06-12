from fastapi import FastAPI
from routers import auth, todos, user, admin
import models
from database import engine
app = FastAPI()
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(user.router)
app.include_router(admin.router)

models.Base.metadata.create_all(bind=engine)
