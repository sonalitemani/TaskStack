from fastapi import APIRouter , Depends , status
from sqlalchemy.orm import Session
from app.tasks import controller
from app.tasks.dtos import TaskSchema ,TaskUpdateSchema ,TaskResponseSchema, Res
from app.database import get_db
import uuid
from typing import List

task_routes = APIRouter(prefix='/tasks', tags=['Tasks'])

@task_routes.post('/create' , response_model=Res[TaskResponseSchema] , status_code=status.HTTP_201_CREATED)
def create_task_route(body: TaskSchema, db:Session = Depends(get_db)):
    task = controller.create_task(body, db)
    return {
        "message": "Task created successfully",
        "status": status.HTTP_201_CREATED,
        "data": task
    }

@task_routes.get('/all_tasks' , response_model=Res[List[TaskResponseSchema]] , status_code=status.HTTP_200_OK)
def get_tasks_route(db:Session = Depends(get_db)):
    tasks = controller.get_tasks(db)
    return {
        "message": "Tasks retrieved successfully",
        "status": status.HTTP_200_OK,
        "data": tasks
    }

@task_routes.get('/{id}' , response_model=Res[TaskResponseSchema] , status_code=status.HTTP_200_OK)
def get_task_by_id_route(id:str , db:Session = Depends(get_db)):
    task = controller.get_task_by_id(id, db)
    return {
        "message": "Task retrieved successfully",
        "status": status.HTTP_200_OK,
        "data": task
    }

@task_routes.patch('/update/{id}' , response_model=Res[TaskResponseSchema] , status_code=status.HTTP_200_OK)
def update_task_route(id:str , body:TaskUpdateSchema , db:Session = Depends(get_db)):
    task = controller.update_task(id, body, db)
    return {
        "message": "Task updated successfully",
        "status": status.HTTP_200_OK,
        "data": task
    }

@task_routes.delete('/delete/{id}' , response_model=Res[None] , status_code=status.HTTP_200_OK)
def delete_task_route(id:str , db:Session= Depends(get_db)):
    controller.delete_task(id, db)
    return {
        "message": "Task deleted successfully",
        "status": status.HTTP_200_OK,
        "data": None
    }
    
