from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserSchema(BaseModel):
    id: UUID | None  # Reference purposes: this id is autogenereated, and won't be passsed in payload.
    name: str
    lastname: str
    email: str
    password: str


class AccountSchema(BaseModel):
    user_id: UUID
    type: str
    card_name: str
    bank: str
    balance: int
    credit_limit: int


class CategorySchema(BaseModel):
    user_id: UUID
    category_name: str
    type: str
    expense_budget: int


class TransactionSchema(BaseModel):
    user_id: UUID
    transaction_date: datetime
    category_id: int
    amount: int
    description: str
    account_id: int
    type: str
