from dotenv import load_dotenv
from src.repositories.account_repo import AccountRepo

load_dotenv()

account = AccountRepo()
values = {
    "user_id": "28fb6f64-2433-4b8e-8a9f-55b72c42e832",
    "type": "credit",
    "card_name": "AMEX Gold Card",
    "bank": "American Express",
    "balance": 20000,
    "credit_limit": 100000
}
account.add_account(**values)
