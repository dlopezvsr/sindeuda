from src.repositories.repository import UserRepo
from dotenv import load_dotenv
from dataclasses import dataclass
from src.models.opeanai_models import PostOperation, OperationValidator
import getpass
import os

from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

load_dotenv()


@dataclass
class LLM:
    llm: ChatOpenAI
    model: str
    temperature: int


@dataclass
class PromptOperations:
    llm: LLM

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
        Once the operation type was validated this function
        will return a dictionary with structured data.
        """
        llm_with_tools = self.llm.bind_tools([PostOperation])
        tool_chain = llm_with_tools | JsonOutputToolsParser()
        operation_type = tool_chain.invoke(user_prompt)
        result = operation_type[0]['args']
        return result


@dataclass
class DatabaseOperations:
    db: SQLDatabase
    llm: LLM

    def operation_processor(self, user_id, operation_information):
        db_query = f"""
        return the IDs of the follwing items according to the corresponding tables 
        from user_id = {user_id}
        Category.id:{operation_information['type']},
        Account.id: {operation_information['card_name']}
        """

        agent_executor = create_sql_agent(self.llm, db=self.db, agent_type="openai-tools", verbose=True)
        result = agent_executor.invoke(db_query)
        # TODO: Pending to validate returned type of result
        return result
