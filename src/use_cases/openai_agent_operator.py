import json
from datetime import datetime

from dotenv import load_dotenv
from dataclasses import dataclass
from src.models.opeanai_models import PostOperation, OperationValidator

from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from src.services.category_service import get_all_categories_service
from src.services.account_service import get_all_accounts_service
from src.services.transaction_service import add_category_service

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
        according fields defined on PostOperation model.
        """
        llm_with_tools = self.llm.bind_tools([PostOperation])
        tool_chain = llm_with_tools | JsonOutputToolsParser()
        operation_type = tool_chain.invoke(user_prompt)
        print(operation_type)
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

    def account_retriever(self, user_id: str):

        db_accounts = get_all_accounts_service(user_id)

        list_of_accounts = [{
            "card_name": tuple(row)[2],
            "bank_name": tuple(row)[3],
            "account_id": tuple(row)[6]
        } for row in db_accounts]

        return list_of_accounts

    def category_retriever(self, user_id: str):

        db_categories = get_all_categories_service(user_id)

        list_of_categories = [{
            "category_name": tuple(row)[1],
            "category_id": tuple(row)[4]} for row in db_categories]

        return list_of_categories

    def rag_id_picker(self, user_id: str, operation_information: dict) -> dict:
        """
        Using the LLM, a description is matched with the name of a category and a card name,
        where only the IDs are returned.

        """
        system_messages = {
            "category": (
                "Based on the following list of categories names, return only and nothing else "
                "than the category_id of the category that most relates with the description"
                "No further text needed."),
            "account": (
                "Based on the following list of card names and bank names, return only and nothing else "
                "than the account_id of the card_name or account that most relates with the description"
                "No further text needed."),
            "agent": (
                "Return two ID's as dictionary with keys account_id and category_id accordingly"
                "if one of them, or neither match with the existing options return null on the key values"
                "No further text needed."
            )

        }
        human_messages = {
            "human_message_category":
                f"categories names: {self.category_retriever(user_id)}, description:{operation_information['description']}",
            "human_message_account":
                f"card and account names: {self.account_retriever(user_id)}, description: {operation_information['card_name']}"
        }
        messages = [
            SystemMessage(content=system_messages["category"]),
            SystemMessage(content=system_messages["account"]),
            HumanMessage(content=human_messages["human_message_category"]),
            HumanMessage(content=human_messages["human_message_account"]),
            SystemMessage(content=system_messages["agent"]),
        ]

        parser = StrOutputParser()
        response = self.llm.invoke(messages)
        result = parser.invoke(response)

        return result

    def operation_processor(self, user_id: str, operation_information: dict) -> dict:
        """
        Processes the given operation information for a specific user and returns the relevant category and account IDs.

        Parameters:
            user_id (int): The ID of the user for whom the operation is being processed.
            operation_information (dict): A dictionary containing information about the operation, including
                 'type': The type of operation/category to filter by.
                 'description': A description to find the best related category.
                 'card_name': The name of the card to find the best matching account.

        Returns:
            dict: A dictionary containing the results with keys 'category'
            and 'account', each mapping to the corresponding IDs.
        """

        if operation_information["transaction_type"] == "GET":
            agent_executor = create_sql_agent(self.llm, db=self.db, agent_type="openai-tools", verbose=True)
            user_db_query = f"""Create a SQL statement from the User query, based on data associated to: user_id = {user_id}. 
            User query: {operation_information["user_query"]}"""
            response = agent_executor.invoke(user_db_query)
            response = {"agent_response": response["output"]}

        else:
            ids_result = json.loads(self.rag_id_picker(user_id, operation_information))
            if ids_result["category_id"] is None or ids_result["account_id"] is None:
                response = "No se encontraron coincidencias, agrega una nueva cuenta o categoría"
            else:
                transaction = {
                    "user_id": user_id,
                    "transaction_date": datetime.now(),
                    "category_id": ids_result["category_id"],
                    "amount": operation_information["amount"],
                    "description": operation_information["description"],
                    "account_id": ids_result["account_id"],
                    "type": operation_information["type"]
                }
                add_category_service(transaction)

                response = "Transaction inserted"

        return response



