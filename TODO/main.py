from fastapi import FastAPI
from .routers import auth,todos,user
app = FastAPI()
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(user.router)

