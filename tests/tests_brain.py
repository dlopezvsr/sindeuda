from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
import os
from dotenv import load_dotenv

load_dotenv()


class LLM:
    def __init__(self, brain, db):
        self.brain: ChatOpenAI = brain
        self.db = db

    def brain(self, user_id, operation_information):
        category_db_query = f"""From following data associated to: user_id = {user_id}, Filter category table by: {operation_information['type']}, then find category_name that has better relation to description: {operation_information['description']} and return the id without further text or questions, can not be null."""
        account_db_query = f"""From following data associated to: user_id = {user_id}, Search into account table, and find the account better fits to: {operation_information['card_name']} and return the id without further text or questions, can not be null."""
        agent_executor = create_sql_agent(self.brain, db=self.db, agent_type="openai-tools", verbose=True)

        category_result = agent_executor.invoke(category_db_query)
        account_result = agent_executor.invoke(account_db_query)
        print(category_result['output'])  # Output: aa10177a-a10e-460a-874b-9b38f4c3ce3b
        print(account_result['output'])  # Output: f115e3b5-5188-4372-903d-b3765ffc2b1c


formatted_data = {'description': 'Lunch with my mom',
                  'card_name': 'AMEX',
                  'type': 'expense'}
user_id = "28fb6f64-2433-4b8e-8a9f-55b72c42e832"
llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0)
db = SQLDatabase.from_uri(os.environ.get("DB_URL"))
start = LLM(llm, db)
start.brain(user_id, formatted_data)

