from dataclasses import dataclass
from sqlalchemy.exc import NoResultFound
from sqlalchemy import create_engine, insert, select
from dotenv import load_dotenv
from uuid import UUID
import os

load_dotenv()
engine = create_engine(os.environ.get("DB_URL"))
