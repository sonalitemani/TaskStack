from fastapi import FastAPI
from app.database import Base, engine
from app.tasks.model import *
from app.tasks.router import task_routes


Base.metadata.create_all(engine)


app = FastAPI()
app.include_router(task_routes)

@app.get('/')
def read_root():
    return {"message": "Welcome to TaskStack API"}
