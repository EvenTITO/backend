from fastapi.encoders import jsonable_encoder
from app.suscriptions.model import SuscriptionStatus
from app.events.crud import EVENT_NOT_FOUND, USER_NOT_FOUNT
from app.suscriptions.schemas import SuscriptorRequestSchema
from ..common import create_headers

PAYMENT_INCOMPLETED = SuscriptionStatus.PAYMENT_INCOMPLETED.value


def test_post_suscription(client, make_suscription):
    suscription_dict = make_suscription()
    id_event = suscription_dict['id_event']
    id_suscriptor = suscription_dict['id_suscriptor']

    response = client.post(
        f"/events/{id_event}/suscriptions",
        json=suscription_dict['json'],
        headers=create_headers(id_suscriptor)
    )
    assert response.status_code == 201
    assert response.json() == id_suscriptor


def test_post_suscription_without_event_fails(client, make_suscription):
    id_event = 'event-does-not-exists'
    suscription_dict = make_suscription(id_event)
    id_suscriptor = suscription_dict['id_suscriptor']

    response = client.post(
        f"/events/{id_event}/suscriptions",
        json=suscription_dict['json'],
        headers=create_headers(id_suscriptor)
    )
    assert response.status_code == 409
    assert response.json()["detail"] == EVENT_NOT_FOUND


def test_post_suscription_without_user_fails(client, make_suscription):
    id_suscriptor = 'user-does-not-exists'
    suscription_dict = make_suscription(id_user=id_suscriptor)
    id_event = suscription_dict['id_event']

    response = client.post(
        f"/events/{id_event}/suscriptions",
        json=suscription_dict['json'],
        headers=create_headers(id_suscriptor)
    )
    assert response.status_code == 409
    assert response.json()["detail"] == USER_NOT_FOUNT
