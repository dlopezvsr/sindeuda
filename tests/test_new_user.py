from dotenv import load_dotenv
from src.repositories.repository import UserRepo

load_dotenv()

user = UserRepo()
values = {
    'user_name': 'Diego',
    'user_last_name': 'Lopez',
    'user_email': 'diego@outions.com',
    'user_password': 'diego123'
}
#user.add_user(**values)


