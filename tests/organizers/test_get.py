from fastapi.encoders import jsonable_encoder
from ..common import create_headers
from app.organizers.schemas import OrganizerRequestSchema


async def test_get_organizers_with_new_organizer(
    client,
    user_data,
    event_creator_data,
    event_from_event_creator
):
    request = OrganizerRequestSchema(
        email_organizer=user_data["email"]
    )
    _ = await client.post(f"/events/{event_from_event_creator}/organizers",
                          json=jsonable_encoder(request),
                          headers=create_headers(event_creator_data["id"]))

    response = await client.get(
        f"/events/{event_from_event_creator}/organizers",
        headers=create_headers(event_creator_data["id"])
    )

    assert response.status_code == 200

    organizers_list = response.json()
    assert len(organizers_list) == 2
    organizers_ids = [organizer['id_organizer']
                      for organizer in organizers_list]
    assert user_data['id'] in organizers_ids


async def test_get_events_with_new_organizer(
    client,
    user_data,
    event_creator_data,
    event_from_event_creator
):
    request = OrganizerRequestSchema(
        email_organizer=user_data["email"]
    )
    _ = await client.post(f"/events/{event_from_event_creator}/organizers",
                          json=jsonable_encoder(request),
                          headers=create_headers(event_creator_data["id"]))

    response = await client.get(
        f"/users/{user_data['id']}/organized-events",
        headers=create_headers(user_data["id"])
    )

    assert response.status_code == 200
    events_list = response.json()
    assert len(events_list) == 1
    assert events_list[0]['id_event'] == event_from_event_creator


async def test_get_events_with_no_organizer(
    client,
    user_data
):
    response = await client.get(
        f"/users/{user_data['id']}/organized-events",
        headers=create_headers(user_data["id"])
    )

    assert response.status_code == 200
    events_list = response.json()
    assert len(events_list) == 0
