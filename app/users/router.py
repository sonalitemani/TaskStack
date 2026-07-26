from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from app.users.dto import (
    UserSchema,
    UserResponseSchema,
    LoginUserSchema,
    LoginResponseSchema,
)
from app.users.controller import register, login_user
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


@user_routes.post("/login", response_model=SuccessResponseSchema[LoginResponseSchema])
def login_user_route(
    body: LoginUserSchema, db: Session = Depends(get_db)
) -> SuccessResponseDict:
    user = login_user(body, db)
    return {
        "message": "User logged in successfully",
        "status": status.HTTP_200_OK,
        "data": user,
    }
