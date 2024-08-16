from fastapi.encoders import jsonable_encoder

from app.schemas.members.member_schema import MemberRequestSchema
from ..commontest import create_headers


async def test_event_creator_can_add_other_user_as_event_organizer(
        client, create_event_creator, create_event_from_event_creator, create_user
):
    request = MemberRequestSchema(
        email=create_user["email"]
    )
    response = await client.post(
        f"/events/{create_event_from_event_creator}/organizers",
        json=jsonable_encoder(request),
        headers=create_headers(create_event_creator["id"])
    )
    assert response.status_code == 201
    assert response.json() == create_user["id"]


async def test_event_organizer_can_add_other_user_as_event_organizer(
        client,
        create_event_from_event_creator,
        organizer_id_from_event,
        create_user
):
    request = MemberRequestSchema(
        email=create_user["email"]
    )
    response = await client.post(
        f"events/{create_event_from_event_creator}/organizers",
        json=jsonable_encoder(request),
        headers=create_headers(organizer_id_from_event)
    )

    assert response.status_code == 201
    assert response.json() == create_user["id"]


async def test_simple_user_tries_add_organizer_fails(
        client, create_user, create_event_from_event_creator
):
    request = MemberRequestSchema(
        email=create_user["email"]
    )
    response = await client.post(
        f"/events/{create_event_from_event_creator}/organizers",
        json=jsonable_encoder(request),
        headers=create_headers(create_user['id'])
    )
    assert response.status_code == 403
