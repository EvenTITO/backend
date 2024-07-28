from app.schemas.events.create_event import CreateEventSchema
from fastapi.encoders import jsonable_encoder
from app.models.event import EventType
import datetime

from app.schemas.events.dates import DateSchema, MandatoryDates
from ..common import create_headers


async def test_post_event(client, admin_data):
    new_event = CreateEventSchema(
        title="Event Title",
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
    new_event = CreateEventSchema(
        title="Event Title",
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
    event = CreateEventSchema(
        title="Another Event Title",
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
    today = datetime.date.today()
    json = jsonable_encoder({
        'title': "Event Title",
        'description': "This is a nice event",
        'dates': [
            DateSchema(
                name=MandatoryDates.START_DATE,
                label='Fecha de Comienzo',
                description='Fecha de comienzo del evento.',
                is_mandatory=True,
                date=today+datetime.timedelta(days=31)
            ).model_dump(mode='json'),
            DateSchema(
                name=MandatoryDates.END_DATE,
                label='Fecha de Finalización',
                description='Fecha de comienzo del evento.',
                is_mandatory=True,
                date=today+datetime.timedelta(days=30)
            ).model_dump(mode='json'),
            DateSchema(
                name=MandatoryDates.SUBMISSION_DEADLINE_DATE,
                label='Fecha de envío de trabajos',
                description='Fecha límite de envío de trabajos.',
                is_mandatory=True
            ).model_dump(mode='json')
        ],
        'event_type': EventType.CONFERENCE,
        'location': 'Paseo Colon 850',
        'tracks': ['math, chemistry, phisics']
    })
    response = await client.post("/events",
                                 json=json,
                                 headers=create_headers(admin_data.id))
    assert response.status_code == 422


async def test_post_event_with_dates(client, admin_data):
    today = datetime.date.today()
    json = jsonable_encoder({
        'title': "Event Title",
        'description': "This is a nice event",
        'dates': [
            DateSchema(
                name=MandatoryDates.START_DATE,
                label='Fecha de Comienzo',
                description='Fecha de comienzo del evento.',
                is_mandatory=True,
                date=today+datetime.timedelta(days=20)
            ).model_dump(mode='json'),
            DateSchema(
                name=MandatoryDates.END_DATE,
                label='Fecha de Finalización',
                description='Fecha de comienzo del evento.',
                is_mandatory=True,
                date=today+datetime.timedelta(days=30)
            ).model_dump(mode='json'),
            DateSchema(
                name=MandatoryDates.SUBMISSION_DEADLINE_DATE,
                label='Fecha de envío de trabajos',
                description='Fecha límite de envío de trabajos.',
                is_mandatory=True
            ).model_dump(mode='json')
        ],
        'event_type': EventType.CONFERENCE,
        'location': 'Paseo Colon 850',
        'tracks': ['math, chemistry, phisics']
    })
    print(json)
    response = await client.post(
        "/events",
        json=json,
        headers=create_headers(admin_data.id)
    )
    assert response.status_code == 201
