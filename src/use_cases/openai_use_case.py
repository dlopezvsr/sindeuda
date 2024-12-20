from src.use_cases.openai_agent_operator import DatabaseOperations, PromptOperations
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai.chat_models.base import ChatOpenAI
from dotenv import load_dotenv
from src.dependency_injection_worker import Container
from dependency_injector.wiring import Provide, inject

load_dotenv()


@inject
def brain(prompt_text: str, llm: ChatOpenAI = Provide[Container.llm]) -> dict:
    """
    Brain function is in charge of executing the methods related with the user prompt,
    where first the prompt is evaluated to define if a POST or GET method will be necessary,
    and then accordingly, the information will be arranged in a dictionary.
    """
    prompt_operations = PromptOperations(llm)
    type_of_transaction = prompt_operations.type_of_operation_validator(prompt_text)
    content_dictionary = {"transaction_type": type_of_transaction}

    if type_of_transaction == "GET":
        content_dictionary.update({"user_query": prompt_text})
    else:
        structured_transaction_info = prompt_operations.post_operation_retriever(prompt_text)
        content_dictionary.update(structured_transaction_info)

    return content_dictionary


@inject
def db_retriever(
        user_id: str,
        prompt_information: dict,
        db: SQLDatabase = Provide[Container.rag_db_connection],
        llm: ChatOpenAI = Provide[Container.llm]) -> dict:
    """
    This function will process a dictionary with information previously structured and complemented by the brain,
    to properly query the DB, receive information, and return and augmented response.

    Return: LLM response to the user prompt.
    Type: Dict
    """
    db_operations = DatabaseOperations(db, llm)
    response = db_operations.operation_processor(user_id, prompt_information)
    return response


async def prompt_processor(prompt_text: str, user_id: str) -> dict:
    brain_response = brain(prompt_text)
    agent_response = db_retriever(user_id, brain_response)
    return agent_response


# TODO: Move this block of code to the section where the services will be used (api routes).
if __name__ == "__main__":
    container = Container()
    container.config.model.from_env("LLM_MODEL", required=True)
    container.config.temperature.from_env("TEMPERATURE", as_=int, default=0)
    container.config.database_uri.from_env("DB_URL")
    container.wire(modules=[__name__])
