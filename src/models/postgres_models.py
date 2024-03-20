from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import ForeignKey, VARCHAR, TIMESTAMP, INT, UUID
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime
import sqlalchemy
import uuid

Base = declarative_base()
metadata = Base.metadata


class Mixin:
    id: Mapped[int] = mapped_column(UUID, primary_key=True, nullable=False, default=uuid.uuid4)


class User(Base, Mixin):
    __tablename__ = "user"
    name: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    last_name: Mapped[str] = mapped_column(VARCHAR(30))
    email: Mapped[str] = mapped_column(VARCHAR(30), unique=True)
    password: Mapped[str] = mapped_column(VARCHAR(50))


class Account(Base, Mixin):
    __tablename__ = "account"
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    type: Mapped[str] = mapped_column(VARCHAR(30))
    card_name: Mapped[str] = mapped_column(VARCHAR(30))
    bank: Mapped[str] = mapped_column(VARCHAR(30))
    balance: Mapped[int] = mapped_column(INT, nullable=False)
    credit_limit: Mapped[int] = mapped_column(INT)


class Category(Base, Mixin):
    __tablename__ = "category"
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    category_name: Mapped[str] = mapped_column(VARCHAR(30))
    type: Mapped[str] = mapped_column(VARCHAR(30))
    expense_budget: Mapped[int] = mapped_column(INT)


class Transaction(Base, Mixin):
    __tablename__ = "transaction"
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    transaction_date: Mapped[datetime] = mapped_column(TIMESTAMP)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    amount: Mapped[int] = mapped_column(INT)
    description: Mapped[str] = mapped_column(VARCHAR(100))
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    type: Mapped[str] = mapped_column(VARCHAR(30))
