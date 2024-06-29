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

    def execute(self, user_id, operation_information):
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
        print(db_query)

        agent_executor = create_sql_agent(self.brain, db=self.db, agent_type="openai-tools", verbose=True)

        agent_executor.invoke(
            db_query
        )


formatted_data = {'amount': 500,
                  'description': 'Dinner with my mom',
                  'card_name': 'AMEX',
                  'type': 'expense'}

user_id = "28fb6f64-2433-4b8e-8a9f-55b72c42e832"
llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0)
db = SQLDatabase.from_uri(os.environ.get("DB_URL"))
start = LLM(ChatOpenAI(), db)

start.execute(user_id, formatted_data)
