import os
from dotenv import load_dotenv

from src.repositories.user_repo import UserRepo
from src.models.api_data_models import UserSchema
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from uuid import UUID

load_dotenv()
pass_encription = CryptContext(schemes=["bcrypt"])
user_operations = UserRepo()


async def user_id_validation(user_id: UUID):
    response = await user_operations.validate_user_id(user_id)
    return response


async def get_user_service(user_email: str):
    response = await user_operations.get_user(user_email)
    return response


async def add_user_service(user_data: UserSchema):
    encrypted_password = pass_encription.hash(user_data.password)
    user_data.password = encrypted_password
    await user_operations.add_user(user_data)


async def authenticate_user(user_email: str, user_password: str):
    encrypted_password = await user_operations.get_user(user_email)
    print(encrypted_password)
    password_validator = pass_encription.verify(user_password, encrypted_password.password)
    return password_validator


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, os.environ.get("SECRET_KEY"), algorithm=os.environ.get('ALGORITHM'))
    return encoded_jwt
