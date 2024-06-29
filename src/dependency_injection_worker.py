from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from langchain_openai.chat_models.base import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
import os


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    llm = providers.Singleton(
        ChatOpenAI,
        model=config.model,
        temperature=config.temperature,
    )
    rag_db_connection = providers.Singleton(
        SQLDatabase.from_uri,
        database_uri=config.database_uri
    )


# TODO: Change this to the correct place where the container will be used and the objects will be injected.

if __name__ == "__main__":
    container = Container()
    container.config.model.from_env("LLM_MODEL", required=True)
    container.config.temperature.from_env("TEMPERATURE", as_=int, default=0)
    container.config.database_uri.from_env("DB_URL")
    container.wire(modules=[__name__])

