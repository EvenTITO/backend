import pytest
from app.events.model import EventStatus, EventType
from app.events.schemas import EventSchema, EventStatusSchema
from fastapi.encoders import jsonable_encoder
from app.organizers.schemas import OrganizerRequestSchema
from app.database.dependencies import get_db
from app.users.model import UserRole
from app.users.schemas import UserSchema, RoleSchema
from app.users.crud import update_role
from app.users.service import get_user
from app.main import app
from app.database.database import SessionLocal, engine, Base
from .common import create_headers, EVENTS, get_user_method, USERS
from uuid import uuid4
from httpx import AsyncClient, ASGITransport


@pytest.fixture(scope="session")
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope="session", autouse=True)
async def setup_database(anyio_backend):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    yield


@pytest.fixture(scope="function", autouse=True)
async def current_session():
    async with engine.connect() as connection:
        async with connection.begin() as transaction:
            session = SessionLocal(bind=connection)
            yield session
            await transaction.rollback()


# Must be async, because the get_db function is async.
@pytest.fixture(scope="function", autouse=True)
async def session_override(current_session):
    async def get_db_session_override():
        yield current_session

    app.dependency_overrides[get_db] = get_db_session_override
    yield
    app.dependency_overrides[get_db] = get_db


@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def user_data(client):
    new_user = UserSchema(
        name="Lio",
        lastname="Messi",
        email="lio_messi@email.com",
    )
    response = await client.post(
        "/users",
        json=jsonable_encoder(new_user),
        headers=create_headers("iuaealdasldanfasdlasd")
    )
    user_data_id = response.json()
    user = await get_user_method(client, user_data_id)
    return user


@pytest.fixture(scope="function")
async def post_users(client):
    ids = []
    for user in USERS:
        id = str(uuid4())
        _ = await client.post(
            "/users",
            json=jsonable_encoder(user),
            headers=create_headers(id)
        )
        ids.append(id)
    return ids


@pytest.fixture(scope="function")
async def admin_data(current_session, client):
    new_user = UserSchema(
        name="Jorge",
        lastname="Benitez",
        email="jbenitez@email.com",
    )
    id_user = "iuaealdasldanfas98298329"
    _ = await client.post(
        "/users",
        json=jsonable_encoder(new_user),
        headers=create_headers(id_user)
    )

    # id_admin = response.json()
    user = await get_user(current_session, id_user)

    user_updated = await update_role(
        current_session, user, UserRole.ADMIN.value
    )
    return user_updated


@pytest.fixture(scope="function")
async def event_creator_data(client, admin_data):
    event_creator = UserSchema(
        name="Juan",
        lastname="Martinez",
        email="jmartinez@email.com",
    )
    user_id = await client.post(
        "/users",
        json=jsonable_encoder(event_creator),
        headers=create_headers("lakjsdeuimx213klasmd3")
    )
    user_id = user_id.json()
    new_role = RoleSchema(
        role=UserRole.EVENT_CREATOR.value
    )
    _ = await client.patch(
        f"/users/{user_id}/roles",
        json=jsonable_encoder(new_role),
        headers=create_headers(admin_data.id)
    )

    event_creator_user = await get_user_method(client, user_id)
    return event_creator_user


@pytest.fixture(scope="function")
async def event_from_event_creator(client, event_creator_data):
    new_event = EventSchema(
        title="Event Creator Event",
        start_date="2024-09-02",
        end_date="2024-09-04",
        description="This is a nice event",
        event_type=EventType.CONFERENCE,
        location='Paseo Colon 850',
        tracks=['math', 'chemistry', 'phisics'],
    )
    response = await client.post(
        "/events",
        json=jsonable_encoder(new_event),
        headers=create_headers(event_creator_data["id"])
    )
    return response.json()


@pytest.fixture(scope="function")
async def event_data(client, admin_data):
    new_event = EventSchema(
        title="Event Title",
        start_date="2024-09-02",
        end_date="2024-09-04",
        description="This is a nice event",
        event_type=EventType.CONFERENCE,
        location='Paseo Colon 850',
        tracks=['math', 'chemistry', 'phisics']
    )
    event_id = await client.post(
        "/events",
        json=jsonable_encoder(new_event),
        headers=create_headers(admin_data.id)
    )
    event_id = event_id.json()

    event_dict = {
        **new_event.model_dump(),
        'id': event_id
    }
    return event_dict


@pytest.fixture(scope="function")
async def all_events_data(client, admin_data):
    ids_events = []
    for event in EVENTS:
        response = await client.post(
            "/events",
            json=jsonable_encoder(event),
            headers=create_headers(admin_data.id)
        )
        ids_events.append(response.json())

    return ids_events


@pytest.fixture(scope="function")
async def inscription_data(client, user_data, event_data):
    id_event = event_data['id']
    response = await client.post(
        f"/events/{id_event}/inscriptions",
        headers=create_headers(user_data["id"])
    )
    id_inscriptor = response.json()
    return {'id_event': id_event, 'id_inscriptor': id_inscriptor}


@pytest.fixture(scope="function")
async def organizer_id_from_event(client, event_creator_data,
                                  event_from_event_creator):
    organizer = UserSchema(
        name="Martina",
        lastname="Rodriguez",
        email="mrodriguez@email.com",
    )
    organizer_id = "frlasdvpqqad08jd"
    await client.post(
        "/users",
        json=jsonable_encoder(organizer),
        headers=create_headers(organizer_id)
    )
    request = OrganizerRequestSchema(
        email_organizer=organizer.email
    )
    await client.post(f"/events/{event_from_event_creator}/organizers",
                      json=jsonable_encoder(request),
                      headers=create_headers(event_creator_data['id']))

    return organizer_id


@pytest.fixture(scope="function")
async def event_started(
        client, event_data, admin_data
):
    status_update = EventStatusSchema(
        status=EventStatus.STARTED
    )
    await client.patch(
        f"/events/{event_data['id']}/status",
        json=jsonable_encoder(status_update),
        headers=create_headers(admin_data.id)
    )
    return event_data['id']
