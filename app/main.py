from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.database import Base, engine
from app.tasks.model import *
from app.tasks.router import task_routes
from app.exceptions import CustomException
from app.utils.exception import register_error_handlers
Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(task_routes)

register_error_handlers(app)

@app.get('/')
def read_root():
    return {"message": "Welcome to TaskStack API"}
