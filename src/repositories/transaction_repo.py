from src.models.api_data_models import TransactionSchema
from src.models.postgres_models import Transaction
from _repository_config import *


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
