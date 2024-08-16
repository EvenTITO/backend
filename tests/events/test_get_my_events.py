from datetime import datetime

from fastapi.encoders import jsonable_encoder

from app.database.models.event import EventType, EventStatus
from app.schemas.events.create_event import CreateEventSchema
from app.schemas.events.event_status import EventStatusSchema
from app.schemas.events.schemas import EventRol
from app.schemas.inscriptions.inscription import InscriptionRequestSchema
from ..commontest import create_headers


async def test_get_my_events_no_events_empty_list(client, create_user):
    response = await client.get("/events/my-events",
                                headers=create_headers(create_user['id']))
    assert len(response.json()) == 0


async def test_get_my_events(client, create_event_started, create_user, admin_data):
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
    )
    organizer_event_id = response.json()
    status_update = EventStatusSchema(
        status=EventStatus.STARTED
    )
    await client.patch(
        f"/events/{organizer_event_id}/status",
        json=jsonable_encoder(status_update),
        headers=create_headers(admin_data.id)
    )
    new_event.title = "Some other Event"
    response = await client.post(
        "/events",
        json=jsonable_encoder(new_event),
        headers=create_headers(create_user['id'])
    )
    organizer_inscripted_event_id = response.json()
    await client.patch(
        f"/events/{organizer_inscripted_event_id}/status",
        json=jsonable_encoder(status_update),
        headers=create_headers(admin_data.id)
    )
    new_attendee_inscription = InscriptionRequestSchema(
        roles=["ATTENDEE"],
        affiliation="Fiuba",
    )
    await client.post(
        f"/events/{organizer_inscripted_event_id}/inscriptions",
        json=jsonable_encoder(new_attendee_inscription),
        headers=create_headers(create_user['id'])
    )
    new_attendee_and_speaker_inscription = InscriptionRequestSchema(
        roles=["ATTENDEE", "SPEAKER"],
        affiliation="Fiuba",
    )
    inscripted_event_id = create_event_started
    await client.post(
        f"/events/{inscripted_event_id}/inscriptions",
        json=jsonable_encoder(new_attendee_and_speaker_inscription),
        headers=create_headers(create_user['id'])
    )

    response = await client.get("/events/my-events", headers=create_headers(create_user['id']))
    events = response.json()
    assert response.status_code == 200
    assert len(events) == 3
    n_events = 0
    for event in events:
        if event['id'] == organizer_event_id:
            assert EventRol.ORGANIZER in event['roles']
            n_events += 1
        elif event['id'] == organizer_inscripted_event_id:
            assert EventRol.ATTENDEE in event['roles']
            assert EventRol.ORGANIZER in event['roles']
            n_events += 1
        elif event['id'] == inscripted_event_id:
            assert EventRol.ATTENDEE in event['roles']
            assert EventRol.SPEAKER in event['roles']
            n_events += 1

    assert n_events == 3
