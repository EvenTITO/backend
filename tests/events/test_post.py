from app.events.schemas import EventSchema
from fastapi.encoders import jsonable_encoder
from app.users.crud import USER_NOT_FOUND_DETAIL
from app.utils.authorization import NOT_PERMISSION_ERROR
from app.events.model import EventType
from datetime import datetime
from ..common import create_headers


def test_post_event(client, make_event):
    event_dict = make_event()

    response = client.post(
        f"/events",
        json=event_dict['json'],
        headers=create_headers(event_dict['id_creator'])
    )
    assert response.status_code == 201
    assert response.json() is not None


def test_post_event_with_admin(
    client,
    make_event,
    make_admin
):
    id_admin = make_admin()['id']
    event_dict = make_event(id_creator=id_admin)

    response = client.post(
        f"/events",
        json=event_dict['json'],
        headers=create_headers(event_dict['id_creator'])
    )
    assert response.status_code == 201
    assert response.json() is not None


def test_post_event_invalid_user(client, make_event):
    event_dict = make_event()

    response = client.post(
        "/events",
        json=event_dict['json'],
        headers=create_headers('invalid-creator-id')
    )

    assert response.status_code == 404
    assert response.json()["detail"] == USER_NOT_FOUND_DETAIL


def test_post_event_user_without_permissions(
    client,
    make_event,
    post_user
):
    id_user = post_user()['id']
    event_dict = make_event()

    response = client.post(
        f"/events",
        json=event_dict['json'],
        headers=create_headers(id_user)
    )

    assert response.status_code == 403
    assert response.json()["detail"] == NOT_PERMISSION_ERROR


def test_post_event_past_dates_fails(
    client,
    make_event
):
    event_dict = make_event(
        start_date="2023-01-01",
        end_date="2023-02-01"
    )

    response = client.post(
        f"/events",
        json=event_dict['json'],
        headers=create_headers(event_dict['id_creator'])
    )
    assert response.status_code == 400


def test_post_event_start_date_gt_end_date_fails(
    client,
    make_event
):
    event_dict = make_event(
        start_date="2024-09-02",
        end_date="2024-09-01"
    )

    response = client.post(
        f"/events",
        json=event_dict['json'],
        headers=create_headers(event_dict['id_creator'])
    )
    assert response.status_code == 400
