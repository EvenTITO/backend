from fastapi.encoders import jsonable_encoder

from app.schemas.members.chair_schema import ChairRequestSchema
from ..commontest import create_headers


async def test_creator_can_add_user_as_chair(
        client,
        create_event_creator,
        create_event_from_event_creator,
        create_user
):
    request = ChairRequestSchema(
        email=create_user["email"],
        tracks=["química", "física", "matemática"],
        role="chair"

    )
    response = await client.post(
        f"/events/{create_event_from_event_creator}/members",
        json=jsonable_encoder(request),
        headers=create_headers(create_event_creator["id"])
    )
    assert response.status_code == 201
    assert response.json() == create_user["id"]


async def test_organizer_can_add_user_as_chair(client, create_organizer, create_event_from_event_creator, create_user):
    request = ChairRequestSchema(
        email=create_user["email"],
        tracks=["química", "física", "matemática"],
        role="chair"
    )
    response = await client.post(
        f"events/{create_event_from_event_creator}/members",
        json=jsonable_encoder(request),
        headers=create_headers(create_organizer)
    )
    assert response.status_code == 201
    assert response.json() == create_user["id"]
