from dotenv import load_dotenv

from src.repositories.account_repo import AccountRepo
from src.models.api_data_models import AccountSchema
from uuid import UUID

load_dotenv()
account_operations = AccountRepo()


async def add_account_service(account: AccountSchema):
    await account_operations.add_account(account)


async def get_account_service(account_id: int, user_id: UUID) -> AccountSchema:
    response = await account_operations.get_account(account_id, user_id)
    return response


async def get_all_accounts_service(user_id: UUID) -> AccountSchema:
    response = await account_operations.get_all_accounts(user_id)
    return response
