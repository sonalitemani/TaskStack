import uuid
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from pydantic_partial import PartialModelMixin


class TaskSchema(PartialModelMixin, BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=30,
    )
    description: str = Field(
        ...,
        min_length=3,
        max_length=100,
    )
    is_completed: bool


TaskUpdateSchema = TaskSchema.model_as_partial()


class TaskResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    title: str
    description: str | None
    is_completed: bool
    created_at: datetime
    updated_at: datetime
