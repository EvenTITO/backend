import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.orm import declarative_base


load_dotenv()
url_database = os.getenv("DATABASE_URL")
engine = create_async_engine(url_database)
SessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
)
Base = declarative_base()
