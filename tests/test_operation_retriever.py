from src.use_cases.openai_service import brain
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai.chat_models.base import ChatOpenAI
from dotenv import load_dotenv
from src.dependency_injection_worker import Container
from dependency_injector.wiring import Provide, inject
import os

load_dotenv()

prompt_expense = "Dinner with my mom $500 AMEX"
prompt_income = "Salary STX $3000 citibanamex"
prompt_information = "What is my highest expense this month?"

formatted_date = {'amount': 500, 'description': 'Dinner with my mom', 'card_name': 'AMEX', 'type': 'expense'}
user_id = "28fb6f64-2433-4b8e-8a9f-55b72c42e832"

print(brain(prompt_information))
