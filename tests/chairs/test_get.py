from fastapi.encoders import jsonable_encoder

from app.schemas.members.chair_schema import ChairRequestSchema
from ..common import create_headers


async def test_get_chairs_with_new_chair(
        client,
        user_data,
        event_creator_data,
        event_from_event_creator
):
    request = ChairRequestSchema(
        email=user_data["email"],
        tracks=["futbol", "tenis"]
    )

    _ = await client.post(f"/events/{event_from_event_creator}/chairs",
                          json=jsonable_encoder(request),
                          headers=create_headers(event_creator_data["id"]))

    response = await client.get(
        f"/events/{event_from_event_creator}/chairs",
        headers=create_headers(event_creator_data["id"])
    )

    assert response.status_code == 200
    chair_list = response.json()
    assert len(chair_list) == 1
    chairs_ids = [chair['user_id'] for chair in chair_list]
    assert user_data['id'] in chairs_ids


async def test_get_chairs_empty(client, event_creator_data, event_from_event_creator):
    response = await client.get(
        f"/events/{event_from_event_creator}/chairs",
        headers=create_headers(event_creator_data["id"])
    )

    assert response.status_code == 200
    chair_list = response.json()
    assert len(chair_list) == 0
