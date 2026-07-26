from fastapi import Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import get_db
import jwt
from jwt.exceptions import InvalidTokenError
from app.config import settings
from sqlalchemy.orm import Session
from app.users.model import UserModel
from app.constants.exception import CustomException

security_scheme = HTTPBearer(auto_error=False)


async def is_authenticated(
    request: Request,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security_scheme),
):
    if not token:
        raise CustomException(
            "you are not authorized to access this resource", status_code=401
        )
    try:
        token_str = token.credentials
        payload = jwt.decode(
            token_str, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id = payload["sub"]
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise CustomException(
                "you are not authorized to access this resource", status_code=401
            )
        request.state.user = user
        return user
    except InvalidTokenError:
        raise CustomException(
            "you are not authorized to access this resource", status_code=401
        )
