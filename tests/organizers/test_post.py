from fastapi.encoders import jsonable_encoder
from app.organizers.schemas import OrganizerRequestSchema
from ..common import create_headers


async def test_event_creator_can_add_other_user_as_event_organizer(
        client, event_creator_data, event_from_event_creator, user_data
):
    request = OrganizerRequestSchema(
        id_organizer=user_data["id"]
    )
    response = await client.post(f"/events/{event_from_event_creator}/organizers",
                                 json=jsonable_encoder(request),
                                 headers=create_headers(event_creator_data["id"]))
    print(response.json())
    assert response.status_code == 201
    assert response.json() == user_data["id"]


async def test_event_organizer_can_add_other_user_as_event_organizer(
        client, organizer_id_from_event, event_from_event_creator, user_data):
    request = OrganizerRequestSchema(
        id_organizer=user_data["id"]
    )
    response = await client.post(f"events/{event_from_event_creator}/organizers",
                                 json=jsonable_encoder(request),
                                 headers=create_headers(organizer_id_from_event))

    assert response.status_code == 201
    assert response.json() == user_data["id"]


async def test_simple_user_tries_add_organizer_fails(
    client, user_data, event_from_event_creator
):
    request = OrganizerRequestSchema(
        id_organizer=user_data["id"]
    )
    response = await client.post(f"/events/{event_from_event_creator}/organizers",
                                 json=jsonable_encoder(request),
                                 headers=create_headers(user_data['id']))
    assert response.status_code == 403
    # assert response.json()['detail'] == EVENT_ORGANIZER_NOT_FOUND
