from app.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from app.tasks.model import TaskModel
from fastapi import HTTPException
import uuid

def create_task(body:TaskSchema , db: Session):
    data = body.model_dump()
    new_task = TaskModel(title =data['title'] , description = data['description'] , is_completed = data['is_completed'])
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task created"}

def get_tasks(db:Session):
    tasks = db.query(TaskModel).all()
    return tasks

def get_task_by_id(id:str , db:Session):
    task = db.query(TaskModel).get(id)
    if not task:
        raise HTTPException(status_code=404 , detail="Task not found")

    return task

def update_task(id:str,body:TaskSchema , db:Session):
    task = get_task_by_id(id, db)
    task.title = body.title
    task.description = body.description
    task.is_completed = body.is_completed
    db.commit()
    db.refresh(task)
    return task

def delete_task(id:str , db:Session):
    task = get_task_by_id(id, db)
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}