from src.models.api_data_models import AccountSchema
from src.models.postgres_models import Account
from _repository_config import *


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

    def get_account(self, account_name: str, user_id: UUID) -> AccountSchema:
        with engine.connect() as connection:
            stmt = select(Account).where(
                (Account.card_name == account_name) &
                (Account.user_id == user_id)
            )
            result = connection.execute(stmt)
            try:
                return result.first()
            except NoResultFound:
                return None