import pytest
from app.events.model import EventType
from app.events.schemas import EventSchema
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from app.database.database import SessionLocal, engine
from app.organizers.schemas import OrganizerRequestSchema
from app.utils.dependencies import get_db
from app.users.model import UserPermission
from app.users.schemas import UserSchema, RoleSchema
from app.users.crud import update_permission
from app.main import app
from .common import create_headers, EVENTS, get_user, USERS
from uuid import uuid4
from app.suscriptions.schemas import SuscriptorRequestSchema


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
    response = client.post("/users",
                           json=jsonable_encoder(new_user),
                           headers=create_headers("iuaealdasldanfasdlasd"))
    user_data_id = response.json()
    return get_user(client, user_data_id)


@pytest.fixture(scope="function")
def post_users(client):
    ids = []
    for user in USERS:
        id = str(uuid4())
        _ = client.post(
            "/users",
            json=jsonable_encoder(user),
            headers=create_headers(id)
        )
        ids.append(id)
    return ids


@pytest.fixture(scope="function")
def admin_data(current_session, client):
    new_user = UserSchema(
        name="Jorge",
        surname="Benitez",
        email="jbenitez@email.com",
    )
    response = client.post(
        "/users",
        json=jsonable_encoder(new_user),
        headers=create_headers("iuaealdasldanfas98298329")
    )

    id_admin = response.json()
    user_updated = update_permission(
        current_session, id_admin, UserPermission.ADMIN.value
    )
    return user_updated


@pytest.fixture(scope="function")
def event_creator_data(client, admin_data):
    event_creator = UserSchema(
        name="Juan",
        surname="Martinez",
        email="jmartinez@email.com",
    )
    user_id = client.post(
        "/users",
        json=jsonable_encoder(event_creator),
        headers=create_headers("lakjsdeuimx213klasmd3")
    ).json()
    new_role = RoleSchema(
        role=UserPermission.EVENT_CREATOR.value
    )
    _ = client.patch(
        f"/users/permissions/{user_id}",
        json=jsonable_encoder(new_role),
        headers=create_headers(admin_data.id)
    )

    event_creator_user = get_user(client, user_id)
    return event_creator_user


@pytest.fixture(scope="function")
def event_from_event_creator(client, event_creator_data):
    new_event = EventSchema(
        title="Event Creator Event",
        start_date="2024-09-02",
        end_date="2024-09-04",
        description="This is a nice event",
        event_type=EventType.CONFERENCE
    )
    response = client.post("/events/",
                           json=jsonable_encoder(new_event),
                           headers=create_headers(event_creator_data["id"]))
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
    event_id = client.post("/events",
                           json=jsonable_encoder(new_event),
                           headers=create_headers(admin_data.id)).json()

    event_dict = {
        **new_event.model_dump(),
        'id': event_id
    }
    return event_dict


@pytest.fixture(scope="function")
def all_events_data(client, admin_data):
    ids_events = []
    for event in EVENTS:
        response = client.post(
            "/events",
            json=jsonable_encoder(event),
            headers=create_headers(admin_data.id)
        )
        ids_events.append(response.json())

    return ids_events


@pytest.fixture(scope="function")
def suscription_data(client, user_data, event_data):
    id_event = event_data['id']
    suscription = SuscriptorRequestSchema(id_suscriptor=user_data["id"])
    id_suscriptor = client.post(
        f"events/{id_event}/suscriptions/",
        json=jsonable_encoder(suscription),
        headers=create_headers(user_data["id"])
    ).json()

    return {'id_event': id_event, 'id_suscriptor': id_suscriptor}


@pytest.fixture(scope="function")
def organizer_id_from_event(client, event_creator_data,
                            event_from_event_creator):
    organizer = UserSchema(
        name="Martina",
        surname="Rodriguez",
        email="mrodriguez@email.com",
    )
    organizer_id = "frlasdvpqqad08jd"
    client.post(
        "/users",
        json=jsonable_encoder(organizer),
        headers=create_headers(organizer_id)
    )
    request = OrganizerRequestSchema(
        id_organizer=organizer_id
    )
    client.post(f"/organizers/{event_from_event_creator['id']}",
                json=jsonable_encoder(request),
                headers=create_headers(event_creator_data["id"]))
    return organizer_id
