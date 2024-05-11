from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
    declarative_base
)


load_dotenv()
url_database = os.getenv("DATABASE_URL")
engine = create_engine(url_database)
SessionLocal = sessionmaker(bind=engine,
                            autocommit=False, autoflush=False)
Base = declarative_base()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
