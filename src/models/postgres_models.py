import sqlalchemy
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Integer, VARCHAR, Float, TIMESTAMP, UUID
from sqlalchemy.orm import mapped_column, Mapped

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = "user"
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    last_name: Mapped[str] = mapped_column(VARCHAR(30))
    email: Mapped[str] = mapped_column(VARCHAR(30))
    password: Mapped[str] = mapped_column(VARCHAR(50))


class Account(Base):
    __tablename__ = "account"
    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    type: Mapped[str] = mapped_column(VARCHAR(30))
    card_name: Mapped[str] = mapped_column(VARCHAR(30))
    bank: Mapped[str] = mapped_column(VARCHAR(30))
    balance: Mapped[float] = mapped_column(Float(2), nullable=False)
    credit_limit: Mapped[float] = mapped_column(Float(2))


class Category(Base):
    __tablename__ = "category"
    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    category_name: Mapped[str] = mapped_column(VARCHAR(30))
    type: Mapped[str] = mapped_column(VARCHAR(30))
    expense_budget: Mapped[str] = mapped_column(Float(2))


class Transaction(Base):
    __tablename__ = "transaction"
    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    transaction_date: Mapped[datetime] = mapped_column(TIMESTAMP())
    category_id: Mapped[str] = mapped_column(ForeignKey("category.id"))
    amount: Mapped[float] = mapped_column(Float(2))
    description: Mapped[str] = mapped_column(VARCHAR(100))
    account_id: Mapped[str] = mapped_column(ForeignKey("account.id"))
    type: Mapped[str] = mapped_column(VARCHAR(30))
