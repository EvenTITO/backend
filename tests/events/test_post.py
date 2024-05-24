from app.events.schemas import EventSchema
from fastapi.encoders import jsonable_encoder
from app.events.model import EventType
from datetime import datetime
from ..common import create_headers


def test_post_event(client, admin_data):
    new_event = EventSchema(
        title="Event Title",
        start_date=datetime(2024, 9, 2),
        end_date=datetime(2024, 9, 3),
        description="This is a nice event",
        event_type=EventType.CONFERENCE,
    )
    response = client.post(
        "/events",
        json=jsonable_encoder(new_event),
        headers=create_headers(admin_data.id)
    )
    assert response.status_code == 201

    response_data = response.json()
    assert response_data is not None


def test_post_event_with_event_creator(client, event_creator_data):
    new_event = EventSchema(
        title="Event Title",
        start_date=datetime(2024, 9, 2),
        end_date=datetime(2024, 9, 3),
        description="This is a nice event",
        event_type=EventType.CONFERENCE,
    )
    response = client.post(
        "/events",
        json=jsonable_encoder(new_event),
        headers=create_headers(event_creator_data['id'])
    )
    assert response.status_code == 201


def test_post_event_invalid_user(client):
    event = EventSchema(
        title="Another Event Title",
        start_date=datetime(2024, 9, 2),
        end_date=datetime(2024, 9, 3),
        description="This is a nice event",
        event_type=EventType.CONFERENCE,
    )

    response = client.post("/events",
                           json=jsonable_encoder(event),
                           headers=create_headers('invalid-creator-id'))

    assert response.status_code == 404
    # assert response.json()["detail"] == USER_NOT_FOUND_DETAIL


def test_post_event_user_without_permissions(client, user_data):
    event = EventSchema(
        title="Another Event Title",
        start_date=datetime(2024, 9, 2),
        end_date=datetime(2024, 9, 3),
        description="This is a nice event",
        event_type=EventType.CONFERENCE,
    )

    response = client.post(
        "/events",
        json=jsonable_encoder(event),
        headers=create_headers(user_data['id'])
    )

    assert response.status_code == 403
    # assert response.json()["detail"] == NOT_PERMISSION_ERROR


def test_post_event_past_dates_fails(client, admin_data):
    end_date_in_the_past = EventSchema(
        title="Event Title",
        start_date="2023-09-02",
        end_date="2023-09-04",
        description="This is a nice event",
        event_type=EventType.CONFERENCE,
    )
    response = client.post("/events",
                           json=jsonable_encoder(end_date_in_the_past),
                           headers=create_headers(admin_data.id))
    assert response.status_code == 400


def test_post_event_start_date_gt_end_date_fails(client, admin_data):
    end_date_in_the_past = EventSchema(
        title="Event Title",
        start_date="2024-09-02",
        end_date="2024-09-01",
        description="This is a nice event",
        event_type=EventType.CONFERENCE,
    )
    response = client.post("/events",
                           json=jsonable_encoder(end_date_in_the_past),
                           headers=create_headers(admin_data.id))
    assert response.status_code == 400
