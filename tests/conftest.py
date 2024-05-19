from app.schemas.suscriptions import UserSuscription
import pytest
from app.models.event import EventType
from app.schemas.events import EventSchema
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from app.database.database import SessionLocal, engine
from app.utils.dependencies import get_db
from app.schemas.users import UserSchema
from app.main import app
from .common import create_headers


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
        name="Lio",
        surname="Messi",
        email="lio_messi@email.com",
    )
    response = client.post("/users/",
                           json=jsonable_encoder(new_user),
                           headers=create_headers("iuaealdasldanfasdlasd"))
    return response.json()


@pytest.fixture(scope="function")
def event_data(client, user_data):
    new_event = EventSchema(
        title="Event Title",
        start_date="2024-09-02",
        end_date="2024-09-04",
        description="This is a nice event",
        event_type=EventType.CONFERENCE
    )
    response = client.post("/events/",
                           json=jsonable_encoder(new_event),
                           headers=create_headers(user_data["id"]))

    return response.json()


@pytest.fixture(scope="function")
def suscription_data(client, user_data, event_data):
    id_event = event_data['id']
    user_suscription = UserSuscription(id=user_data['id'])
    response = client.post(
        f"/suscriptions/{id_event}/",
        json=jsonable_encoder(user_suscription)
    )
    return response.json()
