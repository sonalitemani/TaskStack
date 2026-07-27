from fastapi import APIRouter, Request, Depends, status
from sqlalchemy.orm import Session
from app.tasks import controller
from app.tasks.dtos import TaskSchema, TaskUpdateSchema, TaskResponseSchema
from app.database import get_db
import uuid
from typing import List
from app.constants.response_model import SuccessResponseDict, SuccessResponseSchema
from app.utils.helpers import is_authenticated
from app.users.model import UserModel

task_routes = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    dependencies=[Depends(is_authenticated)],
)


@task_routes.post(
    "/create",
    response_model=SuccessResponseSchema[TaskResponseSchema],
    status_code=status.HTTP_201_CREATED,
)
def create_task_route(
    body: TaskSchema,
    request: Request,
    db: Session = Depends(get_db),
) -> SuccessResponseDict:
    task = controller.create_task(body, db, request)
    return {
        "message": "Task created successfully",
        "status": status.HTTP_201_CREATED,
        "data": task,
    }


@task_routes.get(
    "/all_tasks",
    response_model=SuccessResponseSchema[List[TaskResponseSchema]],
    status_code=status.HTTP_200_OK,
)
def get_tasks_route(
    request: Request, db: Session = Depends(get_db)
) -> SuccessResponseDict:
    tasks = controller.get_tasks(db, request)
    return {
        "message": "Tasks retrieved successfully",
        "status": status.HTTP_200_OK,
        "data": tasks,
    }


@task_routes.get(
    "/{id}",
    response_model=SuccessResponseSchema[TaskResponseSchema],
    status_code=status.HTTP_200_OK,
)
def get_task_by_id_route(id: str, db: Session = Depends(get_db)) -> SuccessResponseDict:
    task = controller.get_task_by_id(id, db)
    return {
        "message": "Task retrieved successfully",
        "status": status.HTTP_200_OK,
        "data": task,
    }


@task_routes.patch(
    "/update/{id}",
    response_model=SuccessResponseSchema[TaskResponseSchema],
    status_code=status.HTTP_200_OK,
)
def update_task_route(
    id: str, body: TaskUpdateSchema, db: Session = Depends(get_db)
) -> SuccessResponseDict:
    task = controller.update_task(id, body, db)
    return {
        "message": "Task updated successfully",
        "status": status.HTTP_200_OK,
        "data": task,
    }


@task_routes.delete(
    "/delete/{id}",
    response_model=SuccessResponseSchema[None],
    status_code=status.HTTP_200_OK,
)
def delete_task_route(id: str, db: Session = Depends(get_db)) -> SuccessResponseDict:
    controller.delete_task(id, db)
    return {
        "message": "Task deleted successfully",
        "status": status.HTTP_200_OK,
        "data": None,
    }
