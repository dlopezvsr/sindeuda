from src.repositories.repository import UserRepo
from dotenv import load_dotenv
import getpass
import os

from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

load_dotenv()

db = SQLDatabase.from_uri(os.environ.get("DB_URL"))


llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0)
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)


agent_executor.invoke(
    "Insert new user"
)
