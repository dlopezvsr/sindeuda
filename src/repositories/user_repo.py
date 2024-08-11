from src.models.api_data_models import UserSchema
from src.models.postgres_models import User
from src.repositories._repository_config import *


@dataclass
class UserRepo:
    def add_user(self, user_data: UserSchema) -> None:
        with engine.connect() as connection:
            stmt = insert(User).values(
                name=user_data.name,
                last_name=user_data.lastname,
                email=user_data.email,
                password=user_data.password
            )
            connection.execute(stmt)
            connection.commit()

    def get_user(self, user_email: int) -> UserSchema:
        """
        Validates if username(email) already exists to register a new user,
        and also for login, and returns
        User Object.
        """
        stmt = select(User).where(User.email == user_email)
        with engine.connect() as connection:
            try:
                result = connection.execute(stmt)
                return result.one()
            except NoResultFound:
                return None

    def validate_user_id(self, user_id: UUID) -> UserSchema:
        """
        Validates with user_id to authenticate,
        once the user already has an account.
        """
        stmt = select(User).where(User.id == user_id)
        with engine.connect() as connection:
            try:
                result = connection.execute(stmt).first()
                return result
            except NoResultFound:
                return None
