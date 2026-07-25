from fastapi import APIRouter , Depends 
from sqlalchemy.orm import Session
from app.tasks import controller
from app.tasks.dtos import TaskSchema ,TaskUpdateSchema
from app.database import get_db
import uuid

task_routes = APIRouter(prefix='/tasks', tags=['Tasks'])

@task_routes.post('/create' , status_code=201)
def create_task_route(body: TaskSchema, db= Depends(get_db)):
    return controller.create_task(body, db)

@task_routes.get('/all_tasks')
def get_tasks_route(db= Depends(get_db)):
    return controller.get_tasks(db)

@task_routes.get('/{id}')
def get_task_by_id_route(id:str , db= Depends(get_db)):
    return controller.get_task_by_id(id, db)

@task_routes.patch('update/{id}')
def update_task_route(id:str , body:TaskUpdateSchema , db= Depends(get_db)):
    return controller.update_task(id, body, db)

@task_routes.delete('delete/{id}')
def delete_task_route(id:str , db= Depends(get_db)):
    return controller.delete_task(id, db)
    
