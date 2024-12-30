from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

from app.core.security import create_access_token
from app.helpers.exception_handler import CustomException
from app.schemas.token_schema import TokenResponse
from app.schemas.user_schema import UserAuth, UserCreate
from app.services.user_service import authenticate_user, register_user
from app.core.database import get_session
router = APIRouter(
)

@router.post("/sign-in",response_model=TokenResponse)
def login(user_data: UserAuth, session: Session = Depends(get_session)):
    user = authenticate_user(session, user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Invalid credentials")

    access_token = create_access_token(data = {"sub":user.email,'role': user.role})
    return TokenResponse(access_token= access_token, token_type="Bearer")

@router.post("/sign-up")
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    try:
        return register_user(session, user_data)
    except Exception as e:
        raise CustomException(http_code = status.HTTP_400_BAD_REQUEST, message = str(e))