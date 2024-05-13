from app.database.database import Base, get_db
from app.main import app
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
import os


client = TestClient(app)
