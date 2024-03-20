from src.repositories.repository import UserRepo
from passlib.context import CryptContext

pass_encription = CryptContext(schemes=["bcrypt"])
user_operations = UserRepo()


def user_validation(user_email: str):
    response = user_operations.validate_user_exists(user_email)
    return response


def add_user_service(user_name: str, user_last_name: str, user_email: str, user_password: str):
    encrypted_password = pass_encription.hash(user_password)
    user_operations.add_user(user_name, user_last_name, user_email, encrypted_password)
