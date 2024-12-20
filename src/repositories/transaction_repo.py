from src.models.api_data_models import TransactionPromptSchema, TransactionSchema
from src.models.postgres_models import Transaction
from src.repositories._repository_config import *


@dataclass
class TransactionRepo:
    async def add_transaction(self, transaction_data: TransactionSchema) -> None:
        async with async_engine.connect() as connection:
            stmt = insert(Transaction).values(
                user_id=transaction_data.user_id,
                transaction_date=transaction_data.transaction_date,
                category_id=transaction_data.category_id,
                amount=transaction_data.amount,
                description=transaction_data.description,
                account_id=transaction_data.account_id,
                type=transaction_data.type
            )
            await connection.execute(stmt)
            await connection.commit()

    async def get_transaction(self, transaction_id: int) -> TransactionSchema:
        async with async_engine.connect() as connection:
            stmt = select(Transaction).where(Transaction.id == transaction_id)
            result = await connection.execute(stmt)
            try:
                return result.first()
            except NoResultFound:
                return None
