from dataclasses import dataclass
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, insert, update, select
from dotenv import load_dotenv
import os

from src.models.postgres_models import User

load_dotenv()
engine = create_engine(os.environ.get("DB_URL"))


@dataclass
class UserRepo:
    # TODO: autogenerate the id, fix model.
    def add_user(self, user_id: str, user_name: str, user_last_name: str, user_email: str, user_password: str) -> None:
        with engine.connect() as connection:
            stmt = insert(User).values(
                id=user_id,
                name=user_name,
                last_name=user_last_name,
                email=user_email,
                password=user_password
            )
            connection.execute(stmt)
            connection.commit()

    def get_user(self):
        pass


@dataclass
class AccountRepo:
    def add_account(self):
        pass

    def get_account(self):
        pass


@dataclass
class CategoryRepo:
    def add_category(self):
        pass

    def get_category(self):
        pass


@dataclass
class TransactionRepo:
    def add_transaction(self):
        pass

    def get_transaction(self):
        pass
