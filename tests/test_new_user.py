from dotenv import load_dotenv
from src.repositories.repository import UserRepo

load_dotenv()

user = UserRepo()
values = {
    "name": "Diego",
    "lastname": "Lopez",
    "email": "diego@sindeuda.com",
    "password": "diejandro174"
}
user.add_user(**values)


