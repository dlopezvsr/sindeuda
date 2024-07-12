from dataclasses import dataclass
from sqlalchemy.exc import NoResultFound
from src.models.api_data_models import UserSchema, AccountSchema, CategorySchema, TransactionSchema
from sqlalchemy import create_engine, insert, select
from dotenv import load_dotenv
from uuid import UUID
import os

from src.models.postgres_models import User, Account, Category

load_dotenv()
engine = create_engine(os.environ.get("DB_URL"))


@dataclass
class UserRepo:
    def add_user(self, user_data: UserSchema) -> None:
        with engine.connect() as connection:
            stmt = insert(User).values(
                name=user_data.name,
                last_name=user_data.lastname,
                email=user_data.email,
                password=user_data.password
            )
            connection.execute(stmt)
            connection.commit()

    def get_user(self, user_email: int) -> UserSchema:
        """
        Validates if username(email) already exists to register a new user,
        and also for login, and returns
        User Object.
        """
        stmt = select(User).where(User.email == user_email)
        with engine.connect() as connection:
            try:
                result = connection.execute(stmt)
                return result.first()
            except NoResultFound:
                return None

    def validate_user_id(self, user_id: UUID) -> UserSchema:
        """
        Validates with user_id to authenticate,
        once the user alredy has an account.
        """
        stmt = select(User).where(User.id == user_id)
        with engine.connect() as connection:
            try:
                result = connection.execute(stmt).first()
                return result
            except NoResultFound:
                return None


@dataclass
class AccountRepo:
    def add_account(self, account_data: AccountSchema) -> None:
        with engine.connect() as connection:
            stmt = insert(Account).values(
                user_id=account_data.user_id,
                type=account_data.type,
                card_name=account_data.card_name,
                bank=account_data.bank,
                balance=account_data.balance,
                credit_limit=account_data.credit_limit
            )
            connection.execute(stmt)
            connection.commit()

    def get_account(self, account_name: str) -> AccountSchema:
        with engine.connect() as connection:
            stmt = select(Account).where(Account.card_name == account_name)
            result = connection.execute(stmt)
            try:
                return result.first()
            except NoResultFound:
                return None


@dataclass
class CategoryRepo:
    def add_category(self, category_data: CategorySchema) -> None:
        with engine.connect() as connection:
            stmt = insert(Category).values(
                user_id=category_data.user_id,
                category_name=category_data.category_name,
                type=category_data.type,
                expense_budget=category_data.expense_budget
            )
            connection.execute(stmt)
            connection.commit()

    def get_category(self, category_name: int) -> CategorySchema:
        with engine.connect() as connection:
            stmt = select(Category).where(Category.category_name == category_name)
            result = connection.execute(stmt)
            try:
                return result.first()
            except NoResultFound:
                return None


@dataclass
class TransactionRepo:
    def add_transaction(self, transaction_data: TransactionSchema) -> None:
        with engine.connect() as connection:
            stmt = insert(Transaction).values(
                user_id=transaction_data.user_id,
                transaction_date=transaction_data.transaction_date,
                category_id=transaction_data.category_id,
                amount=transaction_data.amount,
                description=transaction_data.description,
                account_id=transaction_data.account_id,
                type=transaction_data.type
            )
            connection.execute(stmt)
            connection.commit()

    def get_transaction(self, transaction_id: int) -> TransactionSchema:
        with engine.connect() as connection:
            stmt = select(Transaction).where(Transaction.id == transaction_id)
            result = connection.execute(stmt)
            try:
                return result.first()
            except NoResultFound:
                return None
