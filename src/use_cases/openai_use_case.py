from src.repositories.repository import UserRepo
from dotenv import load_dotenv
import getpass
import os

from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

load_dotenv()

# db = SQLDatabase.from_uri(os.environ.get("DB_URL"))


# llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0)
# agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
# agent_executor.invoke(
#     "What is the most expenisve transaction from last week"
# )

from pydantic import BaseModel, Field
from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser
from langchain_core.output_parsers.openai_tools import PydanticToolsParser


class Operation(BaseModel):
    """Extract information about the transaction of the user,
    if he is preforming an income or expense operation. Get total amount,
    concept, and bank or card name"""

    amount: int = Field(..., description="Total amount of transaction")
    description: str = Field(..., description="Description or concept of transaction")
    card_name: str = Field(..., description="Name of the bank account or card")
    type: str = Field(..., description="Type of operation if income or expense")


llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0)
llm_with_tools = llm.bind_tools([Operation])

tool_chain = llm_with_tools | JsonOutputToolsParser()
result = tool_chain.invoke("Dinner with my mom, $500 with AMEX")

# [{'type': 'Operation', 'args': {'amount': 2000, 'description': 'Salary from STX', 'card_name': 'Citibanamex',
# 'type': 'income'}}]

# [{'type': 'Operation', 'args': {'amount': 500, 'description': 'Dinner with mom', 'card_name': 'AMEX',
# 'type': 'expense'}}]


