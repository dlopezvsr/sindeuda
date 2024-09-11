from dotenv import load_dotenv
from uuid import UUID

from src.repositories.category_repo import CategoryRepo
from src.models.api_data_models import CategorySchema

load_dotenv()
category_operations = CategoryRepo()


async def add_category_service(category: CategorySchema) -> None:
    await category_operations.add_category(category)


async def get_category_service(category_id: UUID, user_id: UUID) -> CategorySchema:
    response = await category_operations.get_category(category_id, user_id)
    return response


async def get_all_categories_service(user_id: UUID) -> CategorySchema:
    response = await category_operations.get_all_categories(user_id)
    return response
