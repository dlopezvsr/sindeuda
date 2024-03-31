from src.use_cases.openai_use_case import LLM, DatabaseOperations, PromptOperations
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

prompt_expense = "Dinner with my mom $500 AMEX"
prompt_income = "Salary STX $3000 citibanamex"
prompt_information = "What is my highest expense this month?"

# llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0)
brain = LLM(ChatOpenAI, "gpt-4-1106-preview", 0)
db = SQLDatabase.from_uri(os.environ.get("DB_URL"))

prompt_operations = PromptOperations(brain)
db_operations = DatabaseOperations(db, brain)

# [{'type': 'Operation', 'args': {'amount': 2000, 'description': 'Salary from STX', 'card_name': 'Citibanamex',
# 'type': 'income'}}]

# [{'type': 'Operation', 'args': {'amount': 500, 'description': 'Dinner with mom', 'card_name': 'AMEX',
# 'type': 'expense'}}]
