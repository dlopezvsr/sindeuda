from dotenv import load_dotenv

from src.repositories.account_repo import AccountRepo
from src.models.api_data_models import AccountSchema
from uuid import UUID

load_dotenv()
account_operations = AccountRepo()


def add_account_servcie(account: AccountSchema):
    account_operations.add_account(account)


def get_account_service(account_id: int, user_id: UUID) -> AccountSchema:
    response = account_operations.get_account(account_id, user_id)
    return response
