from fastapi.encoders import jsonable_encoder
from app.organizers.schemas import OrganizerRequestSchema
from ..common import create_headers


async def test_event_creator_can_remove_other_organizer(
        client, organizer_id_from_event,
        event_from_event_creator, event_creator_data
):
    response = await client.delete(f"/events/{event_from_event_creator}"
                                   f"/organizers/{organizer_id_from_event}",
                                   headers=create_headers(event_creator_data['id']))
    assert response.status_code == 204


async def test_event_organizer_can_remove_other_event_organizer(
        client, organizer_id_from_event,
        event_from_event_creator, user_data
):
    request = OrganizerRequestSchema(
        id_organizer=user_data['id']
    )
    await client.post(f"/events/{event_from_event_creator}/organizers",
                      json=jsonable_encoder(request),
                      headers=create_headers(organizer_id_from_event))

    response = await client.delete(f"/events/{event_from_event_creator}"
                                   f"/organizers/{user_data['id']}",
                                   headers=create_headers(organizer_id_from_event))
    assert response.status_code == 204


async def test_event_organizer_tries_remove_event_creator_fails(
        client, organizer_id_from_event,
        event_from_event_creator, event_creator_data
):
    response = await client.delete(f"/events/{event_from_event_creator}"
                                   f"/organizers/{event_creator_data}",
                                   headers=create_headers(organizer_id_from_event))
    assert response.status_code == 404


async def test_simple_user_tries_remove_organizer_fails(
        client, organizer_id_from_event,
        event_from_event_creator, user_data
):
    response = await client.delete(f"/events/{event_from_event_creator}"
                                   f"/organizers/{organizer_id_from_event}",
                                   headers=create_headers(user_data["id"]))

    assert response.status_code == 404
