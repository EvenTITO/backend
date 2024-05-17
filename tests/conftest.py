from app.schemas.suscriptions import SuscriptionSchema, UserSuscription
import pytest
from app.models.event import EventType
from app.schemas.events import CreateEventSchema
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
        id="iuaealdasldanfasdlasd",
        name="Lio",
        surname="Messi",
        email="lio_messi@email.com",
    )
    response = client.post("/users/", json=jsonable_encoder(new_user))
    return response.json()


@pytest.fixture(scope="function")
def event_data(client, user_data):
    new_event = CreateEventSchema(
        title="Event Title",
        start_date="2024-09-02",
        end_date="2024-09-04",
        description="This is a nice event",
        event_type=EventType.CONFERENCE,
        id_creator=user_data["id"]
    )

    response = client.post("/events/", json=jsonable_encoder(new_event))
    return response.json()


@pytest.fixture(scope="function")
def suscription_data(client, user_data, event_data):
    id_event = event_data['id']
    user_suscription = UserSuscription(id=user_data['id'])
    response = client.post(
        f"/events/{id_event}/suscription", json=jsonable_encoder(user_suscription))
    return response.json()
