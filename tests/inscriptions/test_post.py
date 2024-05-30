from fastapi.encoders import jsonable_encoder
from app.inscriptions.model import InscriptionStatus
from app.inscriptions.schemas import InscriptorRequestSchema
from ..common import create_headers

PAYMENT_INCOMPLETED = InscriptionStatus.PAYMENT_INCOMPLETED.value


async def test_post_inscription(client, user_data, event_data):
    id_event = event_data['id']
    inscription = InscriptorRequestSchema(id_inscriptor=user_data["id"])
    response = await client.post(
        f"/events/{id_event}/inscriptions",
        json=jsonable_encoder(inscription),
        headers=create_headers(user_data["id"])
    )
    assert response.status_code == 201
    assert response.json() == user_data['id']


async def test_post_inscription_without_event_fails(
        client,
        user_data
):
    id_event = "event-does-not-exists"
    inscription = InscriptorRequestSchema(id_inscriptor=user_data["id"])

    response = await client.post(
        f"/events/{id_event}/inscriptions",
        json=jsonable_encoder(inscription),
        headers=create_headers(user_data["id"])
    )
    assert response.status_code == 404
    # assert response.json()["detail"] == EVENT_NOT_FOUND


async def test_post_inscription_without_user_fails(client, event_data):
    id_event = event_data['id']
    id_user_not_exists = 'id-user-does-not-exists'
    inscription = InscriptorRequestSchema(id_inscriptor=id_user_not_exists)
    response = await client.post(
        f"/events/{id_event}/inscriptions",
        json=jsonable_encoder(inscription),
        headers=create_headers(id_user_not_exists)
    )
    assert response.status_code == 404
    # assert response.json()["detail"] == USER_NOT_FOUNT
