from sqlalchemy.orm import Session
from app.users.dto import UserSchema
from pwdlib import PasswordHash
from app.users.model import UserModel
from app.constants.exception import CustomException


password_hash = PasswordHash.recommended()


def get_password_hash(password):
    return password_hash.hash(password)


def register(body: UserSchema, db: Session):
    data = body.model_dump()

    if db.query(UserModel).filter(UserModel.email == data["email"]).first():
        raise CustomException("User with this email already exists", status_code=400)

    if db.query(UserModel).filter(UserModel.username == data["username"]).first():
        raise CustomException("User with this username already exists", status_code=400)

    hashed_pass = get_password_hash(data["password"])

    new_user = UserModel(
        first_name=data["first_name"],
        last_name=data["last_name"],
        username=data["username"],
        email=data["email"],
        hashed_password=hashed_pass,
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise e

    return new_user
