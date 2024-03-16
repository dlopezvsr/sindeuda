import langchain
import getpass
import os

from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI


os.environ["OPENAI_API_KEY"] = getpass.getpass()
db = SQLDatabase.from_uri("")