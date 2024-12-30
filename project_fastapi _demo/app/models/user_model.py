from dataclasses import Field

from httptools.parser.parser import Optional
from sqlalchemy import Column, String, Integer

from ..core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)