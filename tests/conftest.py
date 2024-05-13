import pytest
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from app.database.database import SessionLocal, engine
from app.database.database import get_db
from app.schemas.users import UserSchema
from app.main import app


@pytest.fixture(scope="function")
def client():
    connection = engine.connect()
    transaction = connection.begin()

    db = SessionLocal(bind=connection)

    def get_db_override():
        return db

    app.dependency_overrides[get_db] = get_db_override

    with TestClient(app) as c:
        yield c

    db.close()
    if transaction.is_active:
        transaction.rollback()

    connection.close()


@pytest.fixture(scope="function")
def user_data(client):
    new_user = UserSchema(
        id="iuaealdasldanfasdlasd", name="Lio", surname="Messi", email="lio_messi@email.com"
    )
    response = client.post("/users/", json=jsonable_encoder(new_user))
    return response.json()
