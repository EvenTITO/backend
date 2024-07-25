from app.events.schemas import EventSchema
from fastapi.encoders import jsonable_encoder
from app.models.event import EventType
from datetime import datetime
from ..common import create_headers


async def test_post_event(client, admin_data):
    new_event = EventSchema(
        title="Event Title",
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
        headers=create_headers(admin_data.id)
    )
    assert response.status_code == 201

    response_data = response.json()
    assert response_data is not None


async def test_post_event_with_event_creator(client, event_creator_data):
    new_event = EventSchema(
        title="Event Title",
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
        headers=create_headers(event_creator_data['id'])
    )
    assert response.status_code == 201


async def test_post_event_invalid_user(client):
    event = EventSchema(
        title="Another Event Title",
        start_date=datetime(2024, 9, 2),
        end_date=datetime(2024, 9, 3),
        description="This is a nice event",
        event_type=EventType.CONFERENCE,
        location='Paseo Colon 850',
        tracks=['math', 'chemistry', 'phisics']
    )

    response = await client.post("/events",
                                 json=jsonable_encoder(event),
                                 headers=create_headers('invalid-creator-id'))

    assert response.status_code == 404
    # assert response.json()["detail"] == USER_NOT_FOUND_DETAIL


async def test_post_event_past_dates_fails(client, admin_data):
    json = jsonable_encoder({
        'title': "Event Title",
        'start_date': "2023-09-02",
        'end_date': "2023-09-04",
        'description': "This is a nice event",
        'event_type': EventType.CONFERENCE,
        'location': 'Paseo Colon 850',
        'tracks': 'math, chemistry, phisics'
    })
    response = await client.post("/events",
                                 json=json,
                                 headers=create_headers(admin_data.id))
    assert response.status_code == 422


async def test_post_event_same_dates_fails(client, admin_data):
    json = jsonable_encoder({
        'title': "Event Title",
        'start_date': "2023-09-02",
        'end_date': "2023-09-02",
        'description': "This is a nice event",
        'event_type': EventType.CONFERENCE,
        'location': 'Paseo Colon 850',
        'tracks': 'math, chemistry, phisics'
    })
    response = await client.post("/events",
                                 json=json,
                                 headers=create_headers(admin_data.id))
    assert response.status_code == 422


async def test_post_event_same_without_optional_args(client, admin_data):
    json = jsonable_encoder({
        'title': "Event Title",
        'description': "This is a nice event",
        'event_type': EventType.CONFERENCE,
    })
    response = await client.post("/events",
                                 json=json,
                                 headers=create_headers(admin_data.id))
    assert response.status_code == 201


async def test_post_event_start_date_gt_end_date_fails(client, admin_data):
    json = jsonable_encoder({
        'title': "Event Title",
        'start_date': "2024-09-02",
        'end_date': "2024-09-01",
        'description': "This is a nice event",
        'event_type': EventType.CONFERENCE,
        'location': 'Paseo Colon 850',
        'tracks': 'math, chemistry, phisics'
    })
    response = await client.post("/events",
                                 json=json,
                                 headers=create_headers(admin_data.id))
    assert response.status_code == 422
