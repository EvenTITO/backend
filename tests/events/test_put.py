from fastapi.encoders import jsonable_encoder
from ..common import create_headers


def test_put_event(client, user_data, event_data):
    update_event_data = event_data.copy()
    update_event_data["title"] = "new event"
    update_event_data["end_date"] = "2024-09-05T00:00:00"
    id_event = update_event_data.pop('id')

    response = client.put(
        f"/events/{id_event}",
        json=jsonable_encoder(update_event_data),
        headers=create_headers(user_data["id"])
    )

    assert response.status_code == 204


def test_put_event_with_invalid_end_date_fails(client, admin_data, event_data):
    update_event_data = event_data.copy()
    # start_date = "2024-09-02"
    update_event_data["end_date"] = "2024-08-05T00:00:00"
    id_event = update_event_data.pop('id')
    response = client.put(
        f"/events/{id_event}",
        json=jsonable_encoder(update_event_data),
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 400
