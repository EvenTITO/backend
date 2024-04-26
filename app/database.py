from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


load_dotenv()
url_database = os.getenv("DATABASE_URL")
engine = None
SessionLocal = None
Base = declarative_base()


def get_db():
    if url_database is not None:
        engine = create_engine(url_database)
        SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
        Base.metadata.create_all(bind=engine)
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


