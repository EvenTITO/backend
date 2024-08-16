from fastapi.encoders import jsonable_encoder

from app.schemas.members.chair_schema import ChairRequestSchema
from ..commontest import create_headers


async def test_get_chairs_with_new_chair(
        client,
        create_user,
        event_creator_data,
        event_from_event_creator
):
    request = ChairRequestSchema(
        email=create_user["email"],
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
    unique_chair = chair_list[0]
    assert unique_chair['user_id'] == create_user['id']
    for track in unique_chair['tracks']:
        assert track in ['futbol', 'tenis']


async def test_get_chairs_empty(client, event_creator_data, event_from_event_creator):
    response = await client.get(
        f"/events/{event_from_event_creator}/chairs",
        headers=create_headers(event_creator_data["id"])
    )

    assert response.status_code == 200
    chair_list = response.json()
    assert len(chair_list) == 0
