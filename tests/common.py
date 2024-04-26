from fastapi.testclient import TestClient
from mongomock import MongoClient
from app.main import app
from app.database.mongo import get_db


db = None


def override_get_db():
    global db
    if db is None:
        db = MongoClient().db
    return db



client = TestClient(app)

app.dependency_overrides[get_db] = override_get_db
