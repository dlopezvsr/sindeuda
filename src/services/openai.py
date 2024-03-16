from dotenv import load_dotenv
from src.repositories.repository import UserRepo
import getpass
import os

load_dotenv()

user = UserRepo()
values = {
    'user_id': "123asd",
    'user_name': 'Diego',
    'user_last_name': 'Lopez',
    'user_email': 'diego@outions.com',
    'user_password': 'diego123'
}
user.add_user(**values)
