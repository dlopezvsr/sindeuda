from dotenv import load_dotenv
from src.repositories.repository import CategoryRepo

load_dotenv()

category = CategoryRepo()
values = {
    "user_id": "28fb6f64-2433-4b8e-8a9f-55b72c42e832",
    "category_name": "Restaurants",
    "type": "Expense",  # Income / Expense
    "expense_budget": 6000,
}
category.add_category(**values)
