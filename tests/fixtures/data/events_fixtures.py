import pytest

from fastapi.encoders import jsonable_encoder
from app.database.models.event import EventType, EventStatus
from app.schemas.events.create_event import CreateEventSchema
from app.schemas.events.event_status import EventStatusSchema
from .helper import complete_event_configuration
from ...commontest import create_headers, EVENTS


@pytest.fixture(scope="function")
async def create_event(client, admin_data):
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
async def create_many_events(client, admin_data):
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
async def create_event_started(client, create_event, admin_data):
    status_update = EventStatusSchema(
        status=EventStatus.STARTED
    )

    await complete_event_configuration(client, create_event['id'], admin_data.id)

    await client.patch(
        f"/events/{create_event['id']}/status",
        json=jsonable_encoder(status_update),
        headers=create_headers(admin_data.id)
    )
    return create_event['id']


@pytest.fixture(scope="function")
async def create_many_events_started(client, admin_data):
    ids_events = []
    status_update = EventStatusSchema(
        status=EventStatus.STARTED
    )

    for event in EVENTS:
        response = await client.post(
            "/events",
            json=jsonable_encoder(event),
            headers=create_headers(admin_data.id)
        )
        event_id = response.json()

        await complete_event_configuration(client, event_id, admin_data.id)

        await client.patch(
            f"/events/{event_id}/status",
            json=jsonable_encoder(status_update),
            headers=create_headers(admin_data.id)
        )
        ids_events.append(event_id)

    return ids_events
