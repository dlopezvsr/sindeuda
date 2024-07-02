from src.repositories.repository import UserRepo
from dotenv import load_dotenv
from dataclasses import dataclass
from src.models.opeanai_models import PostOperation, OperationValidator
import getpass
from openai.resources import Completions
import os

from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser
from dependency_injector.wiring import Provide
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

load_dotenv()


@dataclass
class PromptOperations:
    llm: ChatOpenAI

    def type_of_operation_validator(self, user_prompt) -> str:
        """
        Validates the prompt of user and returns the type of
        operation (GET or POST), this will be used later to properly handle
        the response.
        """
        llm_with_tools = self.llm.bind_tools([OperationValidator])
        tool_chain = llm_with_tools | JsonOutputToolsParser()
        operation_type = tool_chain.invoke(user_prompt)
        result = operation_type[0]['args']['type']
        return result

    def post_operation_retriever(self, user_prompt) -> dict:
        """
        Once the operation type (POST or GET) was validated, this function
        will return a dictionary with structured data, divided and organized
        according fileds defined on PostOperation model.
        """
        llm_with_tools = self.llm.bind_tools([PostOperation])
        tool_chain = llm_with_tools | JsonOutputToolsParser()
        operation_type = tool_chain.invoke(user_prompt)
        result = operation_type[0]['args']
        return result


class DatabaseOperations:
    """
    A class to perform operations on a database using an LLM (Language Model) for query processing.
    Attributes:
        db (SQLDatabase): The database connection object.
        Llm (ChatOpenAI): The language model object used for generating SQL queries.
    """

    def __init__(self, db, llm):
        """
        Initializes the DatabaseOperations class with the provided database and language model.
        """
        self.db: SQLDatabase = db
        self.llm: ChatOpenAI = llm

    def operation_processor(self, user_id, operation_information):
        """
        Processes the given operation information for a specific user and returns the relevant category and account IDs.

        Parameters:
            user_id (int): The ID of the user for whom the operation is being processed.
            operation_information (dict): A dictionary containing information about the operation, including:
                - 'type': The type of operation/category to filter by.
                - 'description': A description to find the best related category.
                - 'card_name': The name of the card to find the best matching account.

        Returns:
            dict: A dictionary containing the results with keys 'category'
            and 'account', each mapping to the corresponding IDs.
        """
        category_db_query = f"""From following data associated to: user_id = {user_id}, Filter category table by: {operation_information['type']}, then find category_name that has better relation to description: {operation_information['description']} and return the id without further text or questions, can not be null."""
        account_db_query = f"""From following data associated to: user_id = {user_id}, Search into account table, and find the account better fits to: {operation_information['card_name']} and return the id without further text or questions, can not be null."""
        agent_executor = create_sql_agent(self.llm, db=self.db, agent_type="openai-tools", verbose=True)

        category_result = agent_executor.invoke(category_db_query)
        account_result = agent_executor.invoke(account_db_query)
        result = {"category_id": category_result["output"], "account_id": account_result["output"]}
        return result

