from pydantic import BaseModel


class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str

class UserAuth(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    full_name: str