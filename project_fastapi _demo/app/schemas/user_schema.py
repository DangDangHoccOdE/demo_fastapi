from pydantic import BaseModel


class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str

    class Config:
      from_attributes = True  # Điều này cho phép Pydantic làm việc với các đối tượng SQLAlchemy

class UserAuth(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    full_name: str