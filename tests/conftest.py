import pytest

from fastapi.encoders import jsonable_encoder
from app.database.models.event import EventStatus, EventType
from app.schemas.events.create_event import CreateEventSchema
from app.schemas.events.event_status import EventStatusSchema
from app.schemas.members.member_schema import MemberRequestSchema
from app.schemas.users.user import UserSchema
from .commontest import WORKS, create_headers, EVENTS

from .fixtures.tests_configuration_fixtures import *  # noqa: F401, F403
from .fixtures.storage_mock_fixtures import *  # noqa: F401, F403
from .fixtures.application_setup_fixtures import *  # noqa: F401, F403
from .fixtures.data.users_fixtures import *  # noqa: F401, F403
from .fixtures.data.event_creator_fixtures import *  # noqa: F401, F403


@pytest.fixture(scope="function")
async def event_from_event_creator(client, event_creator_data):
    new_event = CreateEventSchema(
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
    new_event = CreateEventSchema(
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
    event_id = event_data['id']
    response = await client.post(
        f"/events/{event_id}/inscriptions",
        headers=create_headers(user_data["id"])
    )
    inscriptor_id = response.json()
    return {'event_id': event_id, 'inscriptor_id': inscriptor_id}


@pytest.fixture(scope="function")
async def organizer_id_from_event(client, event_creator_data, event_from_event_creator):
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
    request = MemberRequestSchema(
        email=organizer.email
    )
    # invite organizer
    response = await client.post(f"/events/{event_from_event_creator}/organizers",
                                 json=jsonable_encoder(request),
                                 headers=create_headers(event_creator_data['id']))

    assert response.status_code == 201

    # accept organizer invite
    response = await client.patch(f"/events/{event_from_event_creator}/organizers/accept",
                                  headers=create_headers(organizer_id))
    assert response.status_code == 204
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
    event_id = event_data['id']
    for work in WORKS:
        response = await client.post(
            f"/events/{event_id}/works",
            json=jsonable_encoder(work),
            headers=create_headers(user_data["id"])
        )
        work_id = response.json()
        work['id'] = work_id
    return WORKS
