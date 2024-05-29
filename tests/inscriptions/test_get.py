from app.inscriptions.schemas import InscriptorRequestSchema
from fastapi.encoders import jsonable_encoder
from ..common import create_headers


async def test_get_inscription(client, inscription_data):
    id_event = inscription_data['id_event']
    response = await client.get(f"/events/{id_event}/inscriptions")

    assert response.status_code == 200
    inscriptions = response.json()
    assert len(inscriptions) == 1
    assert (inscriptions[0]['id_inscriptor'] ==
            inscription_data['id_inscriptor'])


async def test_user_inscribes_to_two_events(
        client, user_data, all_events_data
):
    inscription = InscriptorRequestSchema(id_inscriptor=user_data["id"])
    _ = await client.post(
        f"/events/{all_events_data[0]}/inscriptions",
        json=jsonable_encoder(inscription),
        headers=create_headers(user_data['id'])
    )

    _ = await client.post(
        f"/events/{all_events_data[1]}/inscriptions",
        json=jsonable_encoder(inscription),
        headers=create_headers(user_data['id'])
    )

    response = await client.get(
        f"/users/{user_data['id']}/inscriptions",
        headers=create_headers(user_data['id'])
    )

    assert response.status_code == 200

    inscriptions_response = response.json()
    assert len(inscriptions_response) == 2
    assert inscriptions_response[0]['id_event'] == all_events_data[0]
    assert inscriptions_response[1]['id_event'] == all_events_data[1]
