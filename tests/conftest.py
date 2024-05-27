import asyncio
from contextlib import AsyncExitStack, ExitStack
import pytest
from app.events.model import EventType
from app.events.schemas import EventSchema
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from app.database.database import SessionLocal, engine
from app.organizers.schemas import OrganizerRequestSchema
from app.utils.dependencies import get_db
from app.users.model import UserRole
from app.users.schemas import UserSchema, RoleSchema
from app.users.crud import update_permission
from app.users.utils import get_user
from app.main import app as main_app
from .common import create_headers, EVENTS, get_user_method, USERS
from uuid import uuid4
from app.suscriptions.schemas import SuscriptorRequestSchema


# @pytest.fixture(scope="function", autouse=True)
# async def current_session():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield


#     async with AsyncExitStack():
#         connection = await engine.connect()
#         transaction = await connection.begin()
#         session = SessionLocal(bind=connection)

#         yield session

#         if connection.in_transaction():
#             await transaction.rollback()

#         await session.close()
#         await connection.close()


# @pytest.fixture(scope="function")
# def client(current_session):

#     async def get_db_override():
#         yield current_session

#     app.dependency_overrides[get_db] = get_db_override

#     with TestClient(app) as c:
#         yield c


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield main_app


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
async def transactional_session():
    async with SessionLocal() as session:
        try:
            await session.begin()
            yield session
        finally:
            await session.rollback()


@pytest.fixture(scope="function")
async def db_session(transactional_session):
    yield transactional_session


@pytest.fixture(scope="function", autouse=True)
async def session_override(app, db_session):
    async def get_db_session_override():
        yield db_session[0]

    app.dependency_overrides[get_db] = get_db_session_override


@pytest.fixture(scope="function")
def user_data(client):
    new_user = UserSchema(
        name="Lio",
        lastname="Messi",
        email="lio_messi@email.com",
    )
    response = client.post("/users",
                           json=jsonable_encoder(new_user),
                           headers=create_headers("iuaealdasldanfasdlasd"))
    user_data_id = response.json()
    return get_user_method(client, user_data_id)


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
        lastname="Benitez",
        email="jbenitez@email.com",
    )
    id_user = "iuaealdasldanfas98298329"
    _ = client.post(
        "/users",
        json=jsonable_encoder(new_user),
        headers=create_headers(id_user)
    )

    # id_admin = response.json()
    user = get_user(current_session, id_user)

    user_updated = update_permission(
        current_session, user, UserRole.ADMIN.value
    )
    return user_updated


@pytest.fixture(scope="function")
def event_creator_data(client, admin_data):
    event_creator = UserSchema(
        name="Juan",
        lastname="Martinez",
        email="jmartinez@email.com",
    )
    user_id = client.post(
        "/users",
        json=jsonable_encoder(event_creator),
        headers=create_headers("lakjsdeuimx213klasmd3")
    ).json()
    new_role = RoleSchema(
        role=UserRole.EVENT_CREATOR.value
    )
    _ = client.patch(
        f"/users/permissions/{user_id}",
        json=jsonable_encoder(new_role),
        headers=create_headers(admin_data.id)
    )

    event_creator_user = get_user_method(client, user_id)
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
    response = client.post("/events",
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
        f"/events/{id_event}/suscriptions/",
        json=jsonable_encoder(suscription),
        headers=create_headers(user_data["id"])
    ).json()

    return {'id_event': id_event, 'id_suscriptor': id_suscriptor}


@pytest.fixture(scope="function")
def organizer_id_from_event(client, event_creator_data,
                            event_from_event_creator):
    organizer = UserSchema(
        name="Martina",
        lastname="Rodriguez",
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
    client.post(f"/events/{event_from_event_creator}/organizers",
                json=jsonable_encoder(request),
                headers=create_headers(event_creator_data['id']))

    return organizer_id
