from pydantic import BaseModel, Field, ConfigDict, EmailStr
import uuid
from datetime import datetime
from pydantic_partial import PartialModelMixin
from typing import Annotated

EmailValidation = Annotated[EmailStr, Field(..., min_length=3, max_length=100)]
PasswordValidation = Annotated[str, Field(..., min_length=8, max_length=255)]


class UserSchema(PartialModelMixin, BaseModel):
    first_name: str = Field(
        ...,
        min_length=3,
        max_length=30,
    )
    last_name: str = Field(
        ...,
        min_length=3,
        max_length=30,
    )
    username: str = Field(
        ...,
        min_length=3,
        max_length=30,
    )
    email: EmailValidation
    password: PasswordValidation


UserUpdateSchema = UserSchema.model_as_partial()


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    first_name: str
    last_name: str
    username: str
    email: str
    created_at: datetime
    updated_at: datetime


class LoginUserSchema(BaseModel):
    email: EmailValidation
    password: PasswordValidation


class LoginResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    access_token: str
    refresh_token: str
    user: UserResponseSchema
