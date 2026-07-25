from app.tasks.dtos import TaskSchema ,TaskUpdateSchema
from sqlalchemy.orm import Session
from app.tasks.model import TaskModel
from app.exceptions import CustomException
import uuid

def create_task(body:TaskSchema , db: Session):
    data = body.model_dump()
    new_task = TaskModel(title =data['title'] , description = data['description'] , is_completed = data['is_completed'])
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_tasks(db:Session):
    tasks = db.query(TaskModel).all()
    return tasks

def get_task_by_id(id:str , db:Session):
    try:
        uuid_obj = uuid.UUID(id)
    except ValueError:
        raise CustomException("Task not found", status_code=404)

    task = db.query(TaskModel).get(uuid_obj)
    if not task:
        raise CustomException("Task not found", status_code=404)

    return task

def update_task(id:str,body:TaskUpdateSchema , db:Session):
    try:
        uuid_obj = uuid.UUID(id)
    except ValueError:
        raise CustomException("Task not found", status_code=404)

    task = db.query(TaskModel).get(uuid_obj)
    if not task:
        raise CustomException("Task not found", status_code=404)
    for key, value in body.model_dump().items():
        if value is not None:
            setattr(task , key , value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(id:str , db:Session):
    task = get_task_by_id(id, db)
    db.delete(task)
    db.commit()
    return None