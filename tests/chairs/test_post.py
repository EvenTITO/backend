from fastapi.encoders import jsonable_encoder

from app.schemas.members.chair_schema import ChairRequestSchema
from app.schemas.members.member_schema import MemberRequestSchema
from ..commontest import create_headers


async def test_creator_can_add_user_as_chair(client, event_creator_data, event_from_event_creator, user_data):
    request = ChairRequestSchema(
        email=user_data["email"],
        tracks=["química", "física", "matemática"]
    )
    response = await client.post(
        f"/events/{event_from_event_creator}/chairs",
        json=jsonable_encoder(request),
        headers=create_headers(event_creator_data["id"])
    )
    print(response.json())
    assert response.status_code == 201
    assert response.json() == user_data["id"]


async def test_organizer_can_add_user_as_chair(client, organizer_id_from_event, event_from_event_creator, user_data):
    request = ChairRequestSchema(
        email=user_data["email"],
        tracks=["química", "física", "matemática"]
    )
    response = await client.post(
        f"events/{event_from_event_creator}/chairs",
        json=jsonable_encoder(request),
        headers=create_headers(organizer_id_from_event)
    )
    assert response.status_code == 201
    assert response.json() == user_data["id"]


async def test_simple_user_tries_add_organizer_fails(client, user_data, event_from_event_creator):
    request = MemberRequestSchema(
        email=user_data["email"],
        tracks=["química", "física", "matemática"]
    )
    response = await client.post(
        f"/events/{event_from_event_creator}/chairs",
        json=jsonable_encoder(request),
        headers=create_headers(user_data['id'])
    )
    assert response.status_code == 403
