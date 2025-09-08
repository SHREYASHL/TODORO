from fastapi import FastAPI
from app.api import auth_routes
from app.api import todo_routes

app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(todo_routes.router)

@app.get("/")
def home():
    return {"message":"hello fastAPI"}