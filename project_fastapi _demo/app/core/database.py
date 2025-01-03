from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import get_settings

settings = get_settings()
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind= engine)
Base = declarative_base()

# Dependency để lấy session
def get_session():
    db = SessionLocal()
    try:
        yield db  # Trả về session để sử dụng trong các endpoint
    finally:
        db.close()  # Đảm bảo đóng session sau khi sử dụng