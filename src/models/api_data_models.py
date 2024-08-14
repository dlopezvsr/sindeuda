from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserSchema(BaseModel):
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
    category_id: UUID
    amount: int
    description: str
    account_id: UUID
    type: str


class TransactionPromptSchema(BaseModel):
    user_id: UUID
    prompt_text: str
