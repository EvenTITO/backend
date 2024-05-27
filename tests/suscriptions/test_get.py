from app.suscriptions.schemas import SuscriptorRequestSchema
from fastapi.encoders import jsonable_encoder
from ..common import create_headers


async def test_get_suscription(client, suscription_data):
    id_event = suscription_data['id_event']
    response = await client.get(f"/events/{id_event}/suscriptions")

    assert response.status_code == 200
    suscriptions = response.json()
    assert len(suscriptions) == 1
    assert (suscriptions[0]['id_suscriptor'] ==
            suscription_data['id_suscriptor'])


async def test_user_suscribes_to_two_events(client, user_data, all_events_data):
    suscription = SuscriptorRequestSchema(id_suscriptor=user_data["id"])
    _ = await client.post(
        f"/events/{all_events_data[0]}/suscriptions",
        json=jsonable_encoder(suscription),
        headers=create_headers(user_data['id'])
    )

    _ = await client.post(
        f"/events/{all_events_data[1]}/suscriptions",
        json=jsonable_encoder(suscription),
        headers=create_headers(user_data['id'])
    )

    response = await client.get(
        f"/users/{user_data['id']}/suscriptions",
        headers=create_headers(user_data['id'])
    )

    assert response.status_code == 200

    suscriptions_response = response.json()
    assert len(suscriptions_response) == 2
    assert suscriptions_response[0]['id_event'] == all_events_data[0]
    assert suscriptions_response[1]['id_event'] == all_events_data[1]
