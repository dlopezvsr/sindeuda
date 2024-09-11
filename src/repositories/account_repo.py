from src.models.api_data_models import AccountSchema
from src.models.postgres_models import Account
from src.repositories._repository_config import *


@dataclass
class AccountRepo:
    async def add_account(self, account_data: AccountSchema) -> None:
        async with async_engine.connect() as connection:
            stmt = insert(Account).values(
                user_id=account_data.user_id,
                type=account_data.type,
                card_name=account_data.card_name,
                bank=account_data.bank,
                balance=account_data.balance,
                credit_limit=account_data.credit_limit
            )
            await connection.execute(stmt)
            await connection.commit()

    async def get_account(self, account_name: str, user_id: UUID) -> AccountSchema:
        async with async_engine.connect() as connection:
            stmt = select(Account).where(
                (Account.card_name == account_name) &
                (Account.user_id == user_id)
            )
            result = await connection.execute(stmt)
            try:
                return result.first()
            except NoResultFound:
                return None

    async def get_all_accounts(self, user_id: UUID) -> AccountSchema:
        async with async_engine.connect() as connection:
            stmt = select(Account).where(
                Account.user_id == user_id
            )
            result = await connection.execute(stmt)
            try:
                return result.all()
            except NoResultFound:
                return None
