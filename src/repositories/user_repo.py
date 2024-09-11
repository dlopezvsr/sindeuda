from src.models.api_data_models import UserSchema
from src.models.postgres_models import User
from src.repositories._repository_config import *


@dataclass
class UserRepo:
    async def add_user(self, user_data: UserSchema) -> None:
        async with async_engine.connect() as connection:
            stmt = insert(User).values(
                name=user_data.name,
                last_name=user_data.lastname,
                email=user_data.email,
                password=user_data.password
            )
            await connection.execute(stmt)
            await connection.commit()

    async def get_user(self, user_email: str) -> UserSchema:
        """
        Validates if username(email) already exists to register a new user,
        and also for login, and returns User Object.
        """
        stmt = select(User).where(User.email == user_email)

        async with async_engine.connect() as session:
            try:
                result = await session.execute(stmt)
                return result.one()
            except NoResultFound:
                return None

    async def validate_user_id(self, user_id: UUID) -> UserSchema:
        """
        Validates with user_id to authenticate,
        once the user already has an account.
        """
        stmt = select(User).where(User.id == user_id)
        async with async_engine.connect() as connection:
            try:
                result = await connection.execute(stmt)
                return result.first()
            except NoResultFound:
                return None
