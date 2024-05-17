from app.models.suscriptions import SuscriptionStatus
from app.schemas.events import CreateEventSchema
from app.schemas.suscriptions import UserSuscription
from fastapi.encoders import jsonable_encoder
from app.models.event import EventType
from app.crud.events import CREATOR_NOT_EXISTS, EVENT_NOT_FOUND, USER_NOT_FOUNT
from datetime import datetime


# ------------------------------- POST TESTS ------------------------------- #


def test_post_suscription(client, user_data, event_data):
    id_event = event_data['id']
    user_suscription = UserSuscription(id=user_data['id'])
    response = client.post(
        f"/events/{id_event}/suscription", json=jsonable_encoder(user_suscription))
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["id_event"] == id_event
    assert response_data["id_suscriptor"] == user_data['id']
    assert response_data["status"] == SuscriptionStatus.PAYMENT_INCOMPLETED.value


def test_post_suscription_without_event_fails(client, user_data):
    id_event = "event-does-not-exists"

    user_suscription = UserSuscription(id=user_data['id'])
    response = client.post(
        f"/events/{id_event}/suscription", json=jsonable_encoder(user_suscription))
    assert response.status_code == 409
    assert response.json()["detail"] == EVENT_NOT_FOUND


def test_post_suscription_without_user_fails(client, event_data):
    id_event = event_data['id']
    user_suscription = UserSuscription(id="user-does-not-exists")
    response = client.post(
        f"/events/{id_event}/suscription", json=jsonable_encoder(user_suscription))
    assert response.status_code == 409
    assert response.json()["detail"] == USER_NOT_FOUNT


# ------------------------------- GET TESTS ------------------------------- #

def test_get_suscription(client, suscription_data):
    id_event = suscription_data['id_event']
    response = client.get(f"/events/{id_event}/suscriptions")
    assert response.status_code == 200
