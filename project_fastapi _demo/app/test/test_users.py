from ast import parse
from datetime import timedelta, datetime, timezone
from http.client import responses
from idlelib.rpc import response_queue

from jose import jwt
from passlib.context import CryptContext
from passlib.handlers.bcrypt import bcrypt
from six import print_
from starlette import status
from app.models.user_model import User
from app.core.database import get_session, settings
from app.dependencies import get_current_user
from app.main import app
from app.services.user_service import authenticate_user, register_user
from app.test.utils import override_get_db, override_get_current_user, client, TestingSessionLocal
from .utils import *
from ..core.security import create_access_token

app.dependency_overrides[get_session] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_users(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {'email': 'haidang@gmail.com', 'full_name': 'Hoang', 'id': 1}]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def test_sign_up(test_user):
    request_data = {
        'full_name':"Hoang",
        'password':pwd_context.hash("admin"),  # Hash mật khẩu
        'email':'haidan1g@gmail.com'
    }

    response = client.post("/auth/sign-up",json=request_data)
    print(response.json())
    assert response.status_code == 200

    db = TestingSessionLocal()
    model = db.query(User).filter(User.email == request_data.get('email')).first()
    assert model.full_name == request_data.get('full_name')
    assert model.email == request_data.get('email')

# def test_get_user_by_email(test_user):
#     response = client.get("/user/1")
#
#     print(response.json())
#
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json() == [{
#         'full_name':"Hoang",
#         'password':bcrypt.hash('admin'),
#         'id':1,
#         'role':'admin',
#         'email':'haidang@gmail.com'
#     }]

# def test_delete_user(test_user):
#     response = client.delete('/user/2')
#     assert response.status_code == 204
#     db = TestingSessionLocal()
#     model = db.query(User).filter(User.id == 1).first()
#     assert model is None

def test_update_user(test_user):  # lỗi
    request_data = {
        'full_name':"Hoang",
        'password':bcrypt.hash('admin'),
        'email':'haidang@gmail.com'
    }

    response = client.put("/user/1",json=request_data)
    assert response.status_code == 200
    db = TestingSessionLocal()
    model = db.query(User).filter(User.email == request_data.get('email')).first()
    assert model.full_name == request_data.get("full_name")

def test_sign_in(test_user):
    db = TestingSessionLocal()

    authenticated_user =  authenticate_user(db, test_user.email, test_user.password)
    assert authenticated_user is None

def test_sign_in_invalid(test_user_invalid):
    db = TestingSessionLocal()

    authenticated_user =  authenticate_user(db, test_user_invalid.email, test_user_invalid.password)
    assert authenticated_user is  None

def test_update_user_not_found(test_user):  # lỗi
    request_data = {
        'full_name':"Hoang",
        'password':bcrypt.hash('admin'),
        'email':'haidang@gmail.com'
    }
    response = client.put("/user/5",json=request_data)
    print(response.json())
    assert response.status_code == 403
    assert response.json() == {'message': '403: You do not have permission to update this user'}

def test_create_access_token():
    email = 'testuser'
    user_id = 1
    role = 'user'

    token = create_access_token(data={'sub':email,'id':user_id,'role':role},)

    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM],
                               options={'verify_signature': False})

    assert decoded_token['sub'] == email
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role

