from fastapi.encoders import jsonable_encoder

from app.schemas.members.chair_schema import ChairRequestSchema
from app.schemas.members.member_schema import MemberRequestSchema
from ..commontest import create_headers


async def test_creator_can_add_user_as_chair(client, event_creator_data, event_from_event_creator, create_user):
    request = ChairRequestSchema(
        email=create_user["email"],
        tracks=["química", "física", "matemática"]
    )
    response = await client.post(
        f"/events/{event_from_event_creator}/chairs",
        json=jsonable_encoder(request),
        headers=create_headers(event_creator_data["id"])
    )
    print(response.json())
    assert response.status_code == 201
    assert response.json() == create_user["id"]


async def test_organizer_can_add_user_as_chair(client, organizer_id_from_event, event_from_event_creator, create_user):
    request = ChairRequestSchema(
        email=create_user["email"],
        tracks=["química", "física", "matemática"]
    )
    response = await client.post(
        f"events/{event_from_event_creator}/chairs",
        json=jsonable_encoder(request),
        headers=create_headers(organizer_id_from_event)
    )
    assert response.status_code == 201
    assert response.json() == create_user["id"]


async def test_simple_user_tries_add_organizer_fails(client, create_user, event_from_event_creator):
    request = MemberRequestSchema(
        email=create_user["email"],
        tracks=["química", "física", "matemática"]
    )
    response = await client.post(
        f"/events/{event_from_event_creator}/chairs",
        json=jsonable_encoder(request),
        headers=create_headers(create_user['id'])
    )
    assert response.status_code == 403
