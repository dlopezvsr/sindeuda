from openai_use_case import DatabaseOperations, PromptOperations

from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai.chat_models.base import ChatOpenAI
from dotenv import load_dotenv
from src.dependency_injection_worker import Container
from dependency_injector.wiring import Provide, inject
import os

load_dotenv()


@inject
def brain(llm: ChatOpenAI = Provide[Container.llm]):
    brain = llm()
    prompt_operations = PromptOperations(brain)
    type_of_transaction = prompt_operations.post_operation_retriever(prompt_expense)
    return type_of_transaction


@inject
def db_retriever(
        user_id: str,
        prompt_expense: str,
        db: SQLDatabase,
        llm: ChatOpenAI = Provide[Container.llm]):

    db_operations = DatabaseOperations(db, llm())
    response = db_operations.operation_processor(user_id, prompt_expense)
    return response['output']


formatted_date = {'amount': 500, 'description': 'Dinner with my mom', 'card_name': 'AMEX', 'type': 'expense'}
user_id = "28fb6f64-2433-4b8e-8a9f-55b72c42e832"
db = SQLDatabase.from_uri(os.environ.get("DB_URL"))

if __name__ == "__main__":
    container = Container()
    container.config.model.from_env("LLM_MODEL", required=True)
    container.config.temperature.from_env("TEMPERATURE", as_=int, default=0)
    container.config.database_uri.from_env("DB_URL")

    container.wire(modules=[__name__])
    print(db_retriever(
        user_id,
        formatted_date,
        db,
        ChatOpenAI
    ))
