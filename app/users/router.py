from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from app.users.dto import UserSchema, UserResponseSchema
from app.users.controller import register
from app.constants.response_model import SuccessResponseDict, SuccessResponseSchema
from app.database import get_db

user_routes = APIRouter(prefix="/user", tags=["Users"])


@user_routes.post("/register", response_model=SuccessResponseSchema[UserResponseSchema])
def register_user(
    body: UserSchema, db: Session = Depends(get_db)
) -> SuccessResponseDict:
    user = register(body, db)
    return {
        "message": "User registered successfully",
        "status": status.HTTP_201_CREATED,
        "data": user,
    }
