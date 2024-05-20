from app.events.schemas import EventSchema
from fastapi.encoders import jsonable_encoder
from app.users.crud import USER_NOT_FOUND_DETAIL
from app.utils.authorization import NOT_PERMISSION_ERROR
from app.events.model import EventType
from app.events.crud import CREATOR_NOT_EXISTS, EVENT_NOT_FOUND
from datetime import datetime
from .common import create_headers

# ------------------------------- POST TESTS ------------------------------- #


def test_post_event(client, admin_data):
    new_event = EventSchema(
        title="Event Title",
        start_date=datetime(2024, 9, 2),
        end_date=datetime(2024, 9, 3),
        description="This is a nice event",
        event_type=EventType.CONFERENCE,
    )
    response = client.post(
        "/events/",
        json=jsonable_encoder(new_event),
        headers=create_headers(admin_data.id)
    )
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["id"] is not None


def test_post_event_with_event_creator(client, event_creator_data):
    new_event = EventSchema(
        title="Event Title",
        start_date=datetime(2024, 9, 2),
        end_date=datetime(2024, 9, 3),
        description="This is a nice event",
        event_type=EventType.CONFERENCE,
    )
    response = client.post(
        "/events/",
        json=jsonable_encoder(new_event),
        headers=create_headers(event_creator_data['id'])
    )
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["title"] == new_event.title


def test_post_event_invalid_user(client):
    event = EventSchema(
        title="Another Event Title",
        start_date=datetime(2024, 9, 2),
        end_date=datetime(2024, 9, 3),
        description="This is a nice event",
        event_type=EventType.CONFERENCE,
    )

    response = client.post("/events/",
                           json=jsonable_encoder(event),
                           headers=create_headers('invalid-creator-id'))

    assert response.status_code == 404
    assert response.json()["detail"] == USER_NOT_FOUND_DETAIL


def test_post_event_user_without_permissions(client, user_data):
    event = EventSchema(
        title="Another Event Title",
        start_date=datetime(2024, 9, 2),
        end_date=datetime(2024, 9, 3),
        description="This is a nice event",
        event_type=EventType.CONFERENCE,
    )

    response = client.post(
        "/events/",
        json=jsonable_encoder(event),
        headers=create_headers(user_data['id'])
    )

    assert response.status_code == 403
    assert response.json()["detail"] == NOT_PERMISSION_ERROR


def test_post_event_past_dates_fails(client, admin_data):
    end_date_in_the_past = EventSchema(
        title="Event Title",
        start_date="2023-09-02",
        end_date="2023-09-04",
        description="This is a nice event",
        event_type=EventType.CONFERENCE,
    )
    response = client.post("/events/",
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
    response = client.post("/events/",
                           json=jsonable_encoder(end_date_in_the_past),
                           headers=create_headers(admin_data.id))
    assert response.status_code == 400


# ------------------------------- GET TESTS ------------------------------- #

def test_get_event(client, event_data):
    response = client.get(f"/events/{event_data['id']}")

    assert response.status_code == 200
    assert response.json()["title"] == event_data["title"]


def test_get_event_not_exists_fails(client):
    id = "this-id-does-not-exist"
    response = client.get(f"/events/{id}")

    assert response.status_code == 404
    assert response.json()["detail"] == EVENT_NOT_FOUND


def test_get_all_events(client, all_events_data):
    _ = all_events_data
    response = client.get("/events/")

    assert response.status_code == 200
    assert len(response.json()["events"]) == 3


# ------------------------------- PUT TESTS ------------------------------- #

def test_put_event(client, user_data, event_data):
    update_event_data = event_data.copy()
    update_event_data["title"] = "new event"
    update_event_data["end_date"] = "2024-09-05T00:00:00"

    response = client.put(
        "/events/",
        json=update_event_data,
        headers=create_headers(user_data["id"])
    )

    assert response.status_code == 200
    assert response.json()["title"] == update_event_data["title"]
    assert response.json()["end_date"] == update_event_data["end_date"]


def test_put_event_with_invalid_end_date_fails(client, admin_data, event_data):
    update_event_data = event_data.copy()
    # start_date = "2024-09-02"
    update_event_data["end_date"] = "2024-08-05T00:00:00"

    response = client.put(
        "/events/",
        json=update_event_data,
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 400

# ------------------------------- DELETE TESTS ------------------------------ #


# TODO: los de delete los hacemos luego de poner endpoints en los suscriptores
# y organizadores
"""
def test_delete_event(client, event_data):

    response = client.delete(f"/events/{event_data['id']}")
    assert response.status_code == 200

def test_delete_user_not_exists(client):
    id = "this-id-does-not-exist"
    response = client.delete(f"/users/{id}")

    assert response.status_code == 404
    assert response.json()["detail"] == USER_NOT_FOUND_DETAIL
"""
