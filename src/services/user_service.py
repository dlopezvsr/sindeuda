import os
from dotenv import load_dotenv

from src.repositories.repository import UserRepo
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from typing import Optional

load_dotenv()
pass_encription = CryptContext(schemes=["bcrypt"])
user_operations = UserRepo()


def user_validation(user_email: str):
    response = user_operations.validate_user_exists(user_email)
    return response


def add_user_service(user_name: str, user_last_name: str, user_email: str, user_password: str):
    encrypted_password = pass_encription.hash(user_password)
    user_operations.add_user(user_name, user_last_name, user_email, encrypted_password)


def authenticate_user(user_email: str, user_password: str):
    encrypted_password = user_validation(user_email)
    password_validator = pass_encription.verify(user_password, encrypted_password.password)
    return password_validator


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, os.environ.get("SECRET_KEY"), algorithm=os.environ.get('ALGORITHM'))
    return encoded_jwt


