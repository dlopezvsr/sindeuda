from src.use_cases.openai_use_case import brain
from dotenv import load_dotenv
from src.dependency_injection_worker import Container

load_dotenv()

prompt_expense = "Dinner with my mom $500 AMEX"
prompt_income = "Salary STX $3000 citibanamex"
prompt_information = "What is my highest expense this month?"


if __name__ == "__main__":
    container = Container()
    container.config.model.from_env("LLM_MODEL", required=True)
    container.config.temperature.from_env("TEMPERATURE", as_=int, default=0)
    container.config.database_uri.from_env("DB_URL")
    container.wire(modules=["src.use_cases.openai_service"])
    structured_information = brain(prompt_expense)
    print(structured_information)
