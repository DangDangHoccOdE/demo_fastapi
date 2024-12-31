from gettext import textdomain

import pytest
from passlib.handlers.bcrypt import bcrypt
from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app.core.database import Base
from app.main import app
from app.models.user_model import User

SQLALCHEMY_DATABASE_URL="sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass= StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'email':'haidang@gmail.com', 'id': 1, 'role':'admin'}

client = TestClient(app)

@pytest.fixture
def test_user():
    user = User(
        full_name="Hoang",
        password=bcrypt.hash('admin'),
        role='admin',
        email='haidang@gmail123.com'
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    db.delete(user)
    db.commit()

@pytest.fixture
def test_user_invalid():
    user = User(
        full_name="Hoang",
        password=bcrypt.hash('admin'),
        id=1,
        role='user',
        email=''
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()