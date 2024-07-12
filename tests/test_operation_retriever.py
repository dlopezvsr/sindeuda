from src.use_cases.openai_service import brain, db_retriever
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
user_id = "28fb6f64-2433-4b8e-8a9f-55b72c42e832"


if __name__ == "__main__":
    container = Container()
    container.config.model.from_env("LLM_MODEL", required=True)
    container.config.temperature.from_env("TEMPERATURE", as_=int, default=0)
    container.config.database_uri.from_env("DB_URL")
    container.wire(modules=["src.use_cases.openai_service"])
    structured_information = brain(prompt_expense)
    print(db_retriever(user_id, structured_information))
