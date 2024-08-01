import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.pool import NullPool


load_dotenv()
url_database = os.getenv("DATABASE_URL")
engine = create_async_engine(url_database, poolclass=NullPool)
SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autocommit=False
)
