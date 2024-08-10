from src.use_cases.openai_use_case import db_retriever
from dotenv import load_dotenv
from src.dependency_injection_worker import Container

load_dotenv()

structured_information = {'transaction_type': 'POST',
                          'amount': 500,
                          'description': 'Dinner with my mom',
                          'card_name': 'AMEX',
                          'type': 'expense'}

user_id = "42e03ad7-beb3-488f-930f-e7c0d28bb1a1"

if __name__ == "__main__":
    container = Container()
    container.config.model.from_env("LLM_MODEL", required=True)
    container.config.temperature.from_env("TEMPERATURE", as_=int, default=0)
    container.config.database_uri.from_env("DB_URL")
    container.wire(modules=["src.use_cases.openai_service"])
    print(db_retriever(user_id, structured_information))
