import pytest
from app.events.model import EventType
from app.events.schemas import EventSchema
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from app.database.database import SessionLocal, engine
from app.utils.dependencies import get_db
from app.users.model import UserPermission
from app.users.schemas import UserSchema, RoleSchema
from app.users.crud import update_permission
from app.main import app
from .common import create_headers, EVENTS


@pytest.fixture(scope="function")
def current_session():
    connection = engine.connect()
    transaction = connection.begin()
    db = SessionLocal(bind=connection)

    yield db

    db.close()
    if transaction.is_active:
        transaction.rollback()

    connection.close()


@pytest.fixture(scope="function")
def client(current_session):

    def get_db_override():
        return current_session

    app.dependency_overrides[get_db] = get_db_override

    with TestClient(app) as c:
        yield c


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
def admin_data(current_session, client):
    new_user = UserSchema(
        name="Jorge",
        surname="Benitez",
        email="jbenitez@email.com",
    )
    response = client.post(
        "/users/",
        json=jsonable_encoder(new_user),
        headers=create_headers("iuaealdasldanfas98298329")
    )

    id_admin = response.json()['id']
    user_updated = update_permission(
        current_session, id_admin, UserPermission.ADMIN.value
    )
    return user_updated


@pytest.fixture(scope="function")
def event_creator_data(client, admin_data, user_data):
    new_role = RoleSchema(
        role=UserPermission.EVENT_CREATOR.value
    )
    response = client.patch(
        f"/users/permissions/{user_data['id']}",
        json=jsonable_encoder(new_role),
        headers=create_headers(admin_data.id)
    )
    return response.json()


@pytest.fixture(scope="function")
def event_data(client, admin_data):
    new_event = EventSchema(
        title="Event Title",
        start_date="2024-09-02",
        end_date="2024-09-04",
        description="This is a nice event",
        event_type=EventType.CONFERENCE
    )
    response = client.post("/events/",
                           json=jsonable_encoder(new_event),
                           headers=create_headers(admin_data.id))

    return response.json()


@pytest.fixture(scope="function")
def all_events_data(client, admin_data):
    responses = []
    for event in EVENTS:
        response = client.post(
            "/events",
            json=jsonable_encoder(event),
            headers=create_headers(admin_data.id)
        )
        responses.append(response.json())

    return responses


@pytest.fixture(scope="function")
def suscription_data(client, user_data, event_data):
    id_event = event_data['id']
    response = client.post(
        f"/suscriptions/{id_event}/",
        headers=create_headers(user_data["id"])
    )
    return response.json()
