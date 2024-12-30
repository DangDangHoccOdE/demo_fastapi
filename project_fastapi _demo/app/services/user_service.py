from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..schemas.user_schema import UserResponse, UserCreate, UserUpdate, UserAuth
from ..crud.user_crud import get_user,get_user_by_email,create_user,update_user,delete_user
from ..models.user_model import User
from ..core.security import get_password_hash, verify_password


def get_all_users(db: Session) -> list[UserResponse]:
    all_user = get_user(db)
    return UserResponse.model_validate(all_user)

def register_user(db: Session, user: UserCreate)-> UserResponse:
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    user_model = create_user(db, User(**user.model_dump()))
    return UserResponse.model_validate(user_model)

def edit_user(db: Session, user_id: int, user_data: UserUpdate) -> UserResponse | None:
    user_updated = update_user(db, user_id, user_data)
    if user_updated is None:
        raise HTTPException(status_code = 404, detail="User not found")
    return UserResponse.model_validate(user_updated)

def authenticate_user(db: Session, email: str, password: str) -> UserAuth | None:
    user = get_user_by_email(db, email)
    if user and verify_password(password, user.password):
        return user
    return None

def delete_user_by_id(db:Session, user_id:int) -> bool:
    return delete_user(db, user_id)