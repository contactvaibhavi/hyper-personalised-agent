import os
import urllib.parse
from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session, Session
from sqlalchemy_utils import create_database, database_exists

load_dotenv()


class Base(DeclarativeBase):
    pass


def init_db(engine: Engine) -> scoped_session[Session]:
    print("init_db")
    if not database_exists(engine.url):
        create_database(engine.url)
    with engine.begin() as connection:
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    print(Base.metadata.tables)
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    ScopedSession = scoped_session(session_factory)
    return ScopedSession


POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fastapi_rag_journal")
encoded_password = urllib.parse.quote_plus(POSTGRES_PASSWORD)

database_url = (
    f"postgresql://{POSTGRES_USERNAME}:{encoded_password}"
    + f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{DATABASE_NAME}"
)

print(database_url)
engine = create_engine(database_url)
DbSession = init_db(engine)

