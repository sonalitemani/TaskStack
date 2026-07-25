from pydantic import BaseModel , Field
from pydantic_partial import PartialModelMixin

class TaskSchema(PartialModelMixin , BaseModel):
    title:str = Field(...,min_length=1, max_length=30)
    description:str = Field(...,min_length=1, max_length=100)
    is_completed:bool 

TaskUpdateSchema = TaskSchema.model_as_partial()