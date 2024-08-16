from datetime import datetime
from fastapi.encoders import jsonable_encoder
from app.database.models.event import EventType
from app.schemas.events.schemas import EventRol
from app.schemas.events.create_event import CreateEventSchema
from ..commontest import create_headers


async def test_get_my_events_no_events_empty_list(client, create_user):
    response = await client.get("/events/my-events",
                                headers=create_headers(create_user['id']))
    assert len(response.json()) == 0


async def test_get_my_events(client, event_data, create_user):
    new_event = CreateEventSchema(
        title="Some Event Title",
        start_date=datetime(2024, 9, 2),
        end_date=datetime(2024, 9, 3),
        description="This is a nice event",
        event_type=EventType.CONFERENCE,
        location='Paseo Colon 850',
        tracks=['math', 'chemistry', 'phisics']
    )
    response = await client.post(
        "/events",
        json=jsonable_encoder(new_event),
        headers=create_headers(create_user['id'])
    )  # Organizer in this event

    organizer_event_id = response.json()

    new_event.title = "Some other Event"
    response = await client.post(
        "/events",
        json=jsonable_encoder(new_event),
        headers=create_headers(create_user['id'])
    )
    organizer_inscripted_event_id = response.json()
    await client.post(
        f"/events/{organizer_inscripted_event_id}/inscriptions",
        headers=create_headers(create_user['id'])
    )  # Organizer & Incripted in this event

    inscripted_event_id = event_data['id']
    await client.post(
        f"/events/{inscripted_event_id}/inscriptions",
        headers=create_headers(create_user['id'])
    )  # Incripted in this event
    response = await client.get("/events/my-events",
                                headers=create_headers(create_user['id']))

    events = response.json()
    print(events)
    n_events = 0
    for event in events:
        if event['id'] == organizer_event_id:
            assert EventRol.ORGANIZER in event['roles']
            n_events += 1
        elif event['id'] == inscripted_event_id:
            assert EventRol.INSCRIPTED in event['roles']
            n_events += 1
        elif event['id'] == organizer_inscripted_event_id:
            assert EventRol.INSCRIPTED in event['roles']
            assert EventRol.ORGANIZER in event['roles']
            n_events += 1

    assert response.status_code == 200
    assert n_events == 3
