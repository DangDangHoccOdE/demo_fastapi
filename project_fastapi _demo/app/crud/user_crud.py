from typing import Annotated, List, Type

from fastapi.params import Depends
from sqlalchemy.orm import Session
from ..models.user_model import User

from app.core.database import SessionLocal
from ..schemas.user_schema import UserUpdate

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def create_user(db: db_dependency,user_model: User) -> User:
    db.add(user_model)
    db.commit()

    return user_model

def get_user(db: db_dependency)-> list[Type[User]]:
    return db.query(User).all()

def get_user_by_email(db: db_dependency, email: str) -> User | None:
     return db.query(User).filter(User.email == email).first()

def update_user(db: db_dependency, user_id: int, user_data: UserUpdate) -> User | None :
    user_model = db.query(User).filter(User.id == user_id).first()
    if user_model:
        db.add(user_model)
        db.commit()
    return None

def delete_user(db: db_dependency, user_id: int) -> bool:
    user_model = db.query(User).filter(User.id == user_id).first()
    if user_model:
        db.delete(user_model)
        db.commit()
        return True
    return False