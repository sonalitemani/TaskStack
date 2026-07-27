from app.tasks.dtos import TaskSchema, TaskUpdateSchema
from sqlalchemy.orm import Session
from app.tasks.model import TaskModel
from app.constants.exception import CustomException
import uuid
from fastapi import Request


def create_task(body: TaskSchema, db: Session, request: Request):
    data = body.model_dump()
    user = getattr(request.state, "user", None)
    new_task = TaskModel(
        title=data["title"],
        description=data["description"],
        is_completed=data["is_completed"],
        user_id=user.id,
    )
    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
    except Exception as e:
        db.rollback()
        raise e
    return new_task


def get_tasks(db: Session, request: Request):
    user = getattr(request.state, "user", None)
    tasks = db.query(TaskModel).all()
    return tasks


def get_task_by_id(id: str, db: Session):
    try:
        uuid_obj = uuid.UUID(id)
    except ValueError:
        raise CustomException("Task not found", status_code=404)

    task = db.query(TaskModel).get(uuid_obj)
    if not task:
        raise CustomException("Task not found", status_code=404)

    return task


def update_task(id: str, body: TaskUpdateSchema, db: Session):
    try:
        uuid_obj = uuid.UUID(id)
    except ValueError:
        raise CustomException("Task not found", status_code=404)

    task = db.query(TaskModel).get(uuid_obj)
    if not task:
        raise CustomException("Task not found", status_code=404)
    for key, value in body.model_dump().items():
        if value is not None:
            setattr(task, key, value)
    try:
        db.commit()
        db.refresh(task)
    except Exception as e:
        db.rollback()
        raise e
    return task


def delete_task(id: str, db: Session):
    task = get_task_by_id(id, db)
    try:
        db.delete(task)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    return None
