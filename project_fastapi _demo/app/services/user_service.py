from fastapi import HTTPException
from passlib.context import CryptContext
from passlib.handlers.bcrypt import bcrypt
from six import print_
from sqlalchemy.orm import Session
from ..schemas.user_schema import UserResponse, UserCreate, UserUpdate, UserAuth
from ..crud.user_crud import get_user,get_user_by_email,create_user,update_user,delete_user
from ..models.user_model import User
from ..core.security import get_password_hash, verify_password

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

def get_all_users(db: Session) -> list[UserResponse]:
    all_users = get_user(db)
 # In ra số lượng người dùng
    print(f"Số lượng người dùng: {len(all_users)}")

    # In ra các đối tượng User (nếu cần)
    for user in all_users:
        print(user)  # In ra mỗi đối tượng User    
    return [UserResponse.model_validate(user) for user in all_users]  # Sử dụng model_validate để chuyển đổi


def register_user(db: Session  , user: UserCreate)-> UserResponse:
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
    if user and bcrypt_context.verify(password, user.password):
        return user
    return None

def delete_user_by_id(db:Session, user_id:int) -> bool:
    return delete_user(db, user_id)