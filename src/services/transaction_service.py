from dotenv import load_dotenv
from uuid import UUID

from src.repositories.transaction_repo import TransactionRepo
from src.models.api_data_models import TransactionSchema

load_dotenv()
transaction_operations = TransactionRepo()


def add_category_service(transaction: dict) -> None:
    transaction_operations.add_transaction(TransactionSchema(**transaction))
