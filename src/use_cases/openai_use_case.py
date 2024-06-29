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
    def __init__(self, db, llm):
        self.db: SQLDatabase = db
        self.llm: ChatOpenAI = llm

    def operation_processor(self, user_id, operation_information):
        db_query = f"""
        From following data associated to:
        user_id = {user_id}
        Filter category table by {operation_information['type']},
        Search in category table, the one better fits to description: {operation_information['description']}
        Search in account table the one better fits to: {operation_information['card_name']}
        return the IDs from the found category and account from user in dictionary structure, 
        exaclty in the following format, no additional text:
        
        {{user_id: value
        account_id: value
        category_id: value}}
        
        """
        agent_executor = create_sql_agent(self.llm, db=self.db, agent_type="openai-tools")
        result = agent_executor.invoke(db_query)
        return result


llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0)
db = SQLDatabase.from_uri(os.environ.get("DB_URL"))
start = DatabaseOperations(db, llm)

formatted_data = {'amount': 500,
                  'description': 'Dinner with my mom',
                  'card_name': 'AMEX',
                  'type': 'expense'}

user_id = "28fb6f64-2433-4b8e-8a9f-55b72c42e832"
start.operation_processor(user_id, formatted_data)
print(start.operation_processor(user_id, formatted_data))


