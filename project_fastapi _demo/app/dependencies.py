import logging
from app.core.database import get_session
from typing import Annotated
from jose import jwt
from fastapi import HTTPException
from passlib.exc import InvalidTokenError
from pydantic import ValidationError
from starlette import status

from fastapi.params import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from app.core.config import get_settings
from app.crud.user_crud import get_user_by_email
from app.models.user_model import User
from app.schemas.token_schema import TokenPayload

logger = logging.getLogger()
reusable_oauth2 = HTTPBearer(scheme_name="Authorization") # Sử dụng HTTPBearer để yêu cầu client gửi token xác thực qua header Authorization.
settings = get_settings()

def get_current_user(http_authorization_credentials: Annotated[HTTPAuthorizationCredentials, Depends(reusable_oauth2)], session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate":"Bearer"}
    )
    try:
        logger.info(http_authorization_credentials.credentials)
        token = http_authorization_credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
        logger.info(token_data)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception

    user = get_user_by_email(session, token_data.sub)
    if user is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    return user

class PermissionRequired:
    def __init__(self, *args):
        self.user = None
        self.permissions = args

    def __call__(self, user: User = Depends(get_current_user)):
        self.user = user
        if self.user.role not in self.permissions:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = f"User {self.user.email} can not access this api"
            )