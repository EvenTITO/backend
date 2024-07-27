from app.storage.schemas import DownloadURLSchema, UploadURLSchema
from app.schemas.users.user import UserSchema
import pytest
from app.models.event import EventStatus, EventType
from app.schemas.schemas import EventSchema, EventStatusSchema
from fastapi.encoders import jsonable_encoder
from app.organizers.schemas import OrganizerRequestSchema
from app.database.dependencies import get_db
from app.models.user import UserRole
from app.schemas.users.user_role import UserRoleSchema
from app.repository.users_crud import update_role
from app.services.users.users_service import create_user, get_user_by_id
from app.main import app
from app.database.database import SessionLocal, engine, Base
from .common import WORKS, create_headers, EVENTS, get_user_method, USERS
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


@pytest.fixture(scope="session")
async def connection(anyio_backend):
    async with engine.connect() as connection:
        yield connection


@pytest.fixture()
async def transaction(connection):
    async with connection.begin() as transaction:
        yield transaction


@pytest.fixture(scope="function")
async def session_override(connection, transaction):
    async def get_db_session_override():
        async_session = SessionLocal(
            bind=connection,
            join_transaction_mode="create_savepoint",
        )
        async with async_session:
            yield async_session

    app.dependency_overrides[get_db] = get_db_session_override
    yield
    del app.dependency_overrides[get_db]

    await transaction.rollback()


@pytest.fixture(scope="function")
async def client(session_override):
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def mock_storage(mocker):
    generate_upload_url_mock = mocker.patch(
        'app.storage.events_storage.generate_signed_upload_url'
    )
    generate_upload_url_mock.return_value = UploadURLSchema(
        upload_url='mocked-url-upload',
        expiration_time_seconds=3600,
        max_upload_size_mb=5
    )

    generate_download_url_mock = mocker.patch(
        'app.storage.storage.generate_signed_read_url'
    )
    generate_download_url_mock.return_value = DownloadURLSchema(
        download_url='mocked-url-download',
        expiration_time_seconds=3600,
    )

    yield


# ------------------------- DATA FIXTURES --------------------------

@pytest.fixture(scope="session")
async def admin_data():
    session = SessionLocal(
        bind=engine,
    )
    new_user = UserSchema(
        name="Jorge",
        lastname="Benitez",
        email="jbenitez@email.com",
    )
    id_user = "iuaealdasldanfas98298329"

    await create_user(session, id_user, new_user)
    user = await get_user_by_id(session, id_user)

    user_updated = await update_role(
        session, user, UserRole.ADMIN.value
    )
    await session.close()
    return user_updated


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
    new_role = UserRoleSchema(
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
async def event_started(client, event_data, admin_data):
    status_update = EventStatusSchema(
        status=EventStatus.STARTED
    )
    await client.patch(
        f"/events/{event_data['id']}/status",
        json=jsonable_encoder(status_update),
        headers=create_headers(admin_data.id)
    )
    return event_data['id']


@pytest.fixture(scope="function")
async def event_works(client, user_data, event_data):
    id_event = event_data['id']
    for work in WORKS:
        response = await client.post(
            f"/events/{id_event}/works",
            json=jsonable_encoder(work),
            headers=create_headers(user_data["id"])
        )
        work_id = response.json()
        work['id'] = work_id
    return WORKS
