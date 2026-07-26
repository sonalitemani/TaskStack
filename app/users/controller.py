from sqlalchemy.orm import Session
from app.users.dto import UserSchema, LoginUserSchema
from pwdlib import PasswordHash
from app.users.model import UserModel
from app.constants.exception import CustomException
import jwt
from app.config import settings
from datetime import timedelta, datetime, timezone

password_hash = PasswordHash.recommended()

JWT_SECRET = settings.JWT_SECRET
ALGORITHM = settings.JWT_ALGORITHM
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
JWT_REFRESH_TOKEN_EXPIRE_MINUTES = settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES


def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


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


def login_user(body: LoginUserSchema, db: Session):
    user = db.query(UserModel).filter(UserModel.email == body.email).first()
    if not user:
        raise CustomException("User not found", status_code=404)

    if not verify_password(body.password, user.hashed_password):
        raise CustomException("Invalid password", status_code=401)

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "refresh_token": refresh_token, user: user}
