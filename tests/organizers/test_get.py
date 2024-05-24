from fastapi.encoders import jsonable_encoder
from ..common import create_headers
from app.organizers.schemas import OrganizerRequestSchema


def test_get_organizers_with_new_organizer(
    client,
    post_organizers
):
    organizers_dicts = post_organizers(n=2)

    response = client.get(
        f"/events/{organizers_dicts[0]['id_event']}/organizers",
        headers=create_headers(organizers_dicts[0]['id_organizer'])
    )

    assert response.status_code == 200

    organizers_list = response.json()
    assert len(organizers_list) == 2


def test_get_events_with_new_organizer(
    client,
    user_data,
    event_creator_data,
    event_from_event_creator
):
    request = OrganizerRequestSchema(
        id_organizer=user_data["id"]
    )
    _ = client.post(f"/events/{event_from_event_creator}/organizers",
                    json=jsonable_encoder(request),
                    headers=create_headers(event_creator_data["id"]))

    response = client.get(
        f"/users/{user_data['id']}/organized-events",
        headers=create_headers(user_data["id"])
    )

    assert response.status_code == 200
    events_list = response.json()
    assert len(events_list) == 1
    assert events_list[0]['id_event'] == event_from_event_creator


def test_get_events_with_no_organizer(
    client,
    user_data
):
    response = client.get(
        f"/users/{user_data['id']}/organized-events",
        headers=create_headers(user_data["id"])
    )

    assert response.status_code == 200
    events_list = response.json()
    assert len(events_list) == 0
