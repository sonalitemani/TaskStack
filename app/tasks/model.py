from sqlalchemy import Column , Integer , String , Boolean , DateTime , Uuid
from  app.database import Base
from datetime import datetime , UTC
import uuid

class TaskModel(Base):
    __tablename__ = 'tasks'

    id = Column(Uuid, primary_key=True , default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String)
    is_completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    

