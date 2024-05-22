from fastapi.encoders import jsonable_encoder
from app.suscriptions.model import SuscriptionStatus
from app.events.crud import EVENT_NOT_FOUND, USER_NOT_FOUNT
from app.suscriptions.schemas import SuscriptorRequestSchema
from ..common import create_headers

PAYMENT_INCOMPLETED = SuscriptionStatus.PAYMENT_INCOMPLETED.value


def test_post_suscription(client, user_data, event_data):
    id_event = event_data['id']
    suscription = SuscriptorRequestSchema(id_suscriptor=user_data["id"])
    response = client.post(
        f"/events/{id_event}/suscriptions",
        json=jsonable_encoder(suscription),
        headers=create_headers(user_data["id"])
    )
    assert response.status_code == 201
    assert response.json() == user_data['id']


def test_post_suscription_without_event_fails(
        client,
        user_data
):
    id_event = "event-does-not-exists"
    suscription = SuscriptorRequestSchema(id_suscriptor=user_data["id"])

    response = client.post(
        f"/events/{id_event}/suscriptions",
        json=jsonable_encoder(suscription),
        headers=create_headers(user_data["id"])
    )
    assert response.status_code == 409
    assert response.json()["detail"] == EVENT_NOT_FOUND


def test_post_suscription_without_user_fails(client, event_data):
    id_event = event_data['id']
    id_user_not_exists = 'id-user-does-not-exists'
    suscription = SuscriptorRequestSchema(id_suscriptor=id_user_not_exists)
    response = client.post(
        f"/events/{id_event}/suscriptions",
        json=jsonable_encoder(suscription),
        headers=create_headers(id_user_not_exists)
    )
    assert response.status_code == 409
    assert response.json()["detail"] == USER_NOT_FOUNT
