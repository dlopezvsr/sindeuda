from pydantic import BaseModel
from datetime import datetime


class UserSchema:
    name: str
    lastname: str
    email: str
    password: str


class AccountSchema:
    user_id: int
    type: str
    card_name: str
    bank: str
    balance: int
    credit_limit: int


class CategorySchema:
    user_id: int
    category_name: str
    type: str
    expense_budget: int


class TransactionSchema:
    user_id: int
    transaction_date: datetime
    category_id: int
    amount: int
    description: str
    account_id: int
    type: str
