from src.models.api_data_models import CategorySchema
from src.models.postgres_models import Category
from src.repositories._repository_config import *


@dataclass
class CategoryRepo:
    def add_category(self, category_data: CategorySchema) -> None:
        with engine.connect() as connection:
            stmt = insert(Category).values(
                user_id=category_data.user_id,
                category_name=category_data.category_name,
                type=category_data.type,
                expense_budget=category_data.expense_budget
            )
            connection.execute(stmt)
            connection.commit()

    def get_category(self, category_name: int, user_id: UUID) -> CategorySchema:
        with engine.connect() as connection:
            stmt = select(Category).where(
                (Category.category_name == category_name) &
                (Category.user_id == user_id)
            )

            result = connection.execute(stmt)
            try:
                return result.first()
            except NoResultFound:
                return None

    def get_all_categories(self, user_id: UUID) -> CategorySchema:
        with engine.connect() as connection:
            stmt = select(Category).where(
                Category.user_id == user_id
            )
            result = connection.execute(stmt)
            try:
                return result.all()
            except NoResultFound:
                return None