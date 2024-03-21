from dataclasses import dataclass
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, insert, update, select, func
from dotenv import load_dotenv
import os

from src.models.postgres_models import User, Account

load_dotenv()
engine = create_engine(os.environ.get("DB_URL"))


@dataclass
class UserRepo:
    def add_user(self, user_name: str, user_last_name: str, user_email: str, user_password: str) -> None:
        with engine.connect() as connection:
            stmt = insert(User).values(
                name=user_name,
                last_name=user_last_name,
                email=user_email,
                password=user_password
            )
            connection.execute(stmt)
            connection.commit()

    def get_user(self, user_id: int):
        stmt = select(User).where(User.id == user_id)
        with engine.connect() as connection:
            result = connection.execute(stmt)
            return result.first()

    def validate_user_exists(self, user_email: int):
        stmt = select(User).where(User.email == user_email)
        with engine.connect() as connection:
            result = connection.execute(stmt)
            return result.first()


@dataclass
class AccountRepo:
    def add_account(self):
        with engine.connect() as connection:
            stmt = insert(Account).values(
            )
            connection.execute(stmt)
            connection.commit()

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
