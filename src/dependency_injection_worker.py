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
