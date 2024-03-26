import os
from dotenv import load_dotenv

from src.repositories.repository import AccountRepo
from src.application.api_data_models import UserSchema, AccountSchema, CategorySchema, TransactionSchema

load_dotenv()
account_operations = AccountRepo()


def add_account_servcie(account: AccountSchema):
    account_operations.add_account(account)


def get_account_service(account_id: int) -> AccountSchema:
    response = account_operations.get_account(account_id)
    return response
