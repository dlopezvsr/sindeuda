from dotenv import load_dotenv
from uuid import UUID

from src.repositories.repository import CategoryRepo
from src.models.api_data_models import CategorySchema

load_dotenv()
category_operations = CategoryRepo()


def add_category_service(category: CategorySchema) -> None:
    category_operations.add_category(category)


def get_category_service(category_id: UUID, user_id: UUID) -> CategorySchema:
    response = category_operations.get_category(category_id, user_id)
    return response
