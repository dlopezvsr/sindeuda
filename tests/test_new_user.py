from dotenv import load_dotenv
from src.repositories.user_repo import UserRepo

load_dotenv()

user = UserRepo()
values = {
    "name": "Diego",
    "lastname": "Lopez",
    "email": "diego@sindeuda.com",
    "password": "diejandro174"
}
user.add_user(**values)


