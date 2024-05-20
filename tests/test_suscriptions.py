from app.suscriptions.model import SuscriptionStatus
from app.events.crud import EVENT_NOT_FOUND, USER_NOT_FOUNT
from .common import create_headers


PAYMENT_INCOMPLETED = SuscriptionStatus.PAYMENT_INCOMPLETED.value

# ------------------------------- POST TESTS ------------------------------- #


def test_post_suscription(client, user_data, event_data):
    id_event = event_data['id']
    response = client.post(
        f"/suscriptions/{id_event}/",
        headers=create_headers(user_data["id"])
    )
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["id_event"] == id_event
    assert response_data["id_suscriptor"] == user_data['id']
    assert response_data["status"] == PAYMENT_INCOMPLETED


def test_post_suscription_without_event_fails(
        client,
        user_data
):
    id_event = "event-does-not-exists"

    response = client.post(
        f"/suscriptions/{id_event}/",
        headers=create_headers(user_data["id"])
    )
    assert response.status_code == 409
    assert response.json()["detail"] == EVENT_NOT_FOUND


def test_post_suscription_without_user_fails(client, event_data):
    id_event = event_data['id']

    response = client.post(
        f"/suscriptions/{id_event}/",
        headers=create_headers('id-user-does-not-exists')
    )
    assert response.status_code == 409
    assert response.json()["detail"] == USER_NOT_FOUNT


# ------------------------------- GET TESTS ------------------------------- #


def test_get_suscription(client, suscription_data):
    id_event = suscription_data['id_event']
    response = client.get(f"/suscriptions/events/{id_event}/")
    assert response.status_code == 200


def test_user_suscribes_to_two_events(client, user_data, all_events_data):
    _ = client.post(
        f"/suscriptions/{all_events_data[0]['id']}",
        headers=create_headers(user_data['id'])
    )

    _ = client.post(
        f"/suscriptions/{all_events_data[1]['id']}",
        headers=create_headers(user_data['id'])
    )

    response = client.get(
        f"/suscriptions/users/",
        headers=create_headers(user_data['id'])
    )

    assert response.status_code == 200

    suscriptions_response = response.json()['suscriptions']
    assert len(suscriptions_response) == 2
    assert suscriptions_response[0]['id_suscriptor'] == user_data['id']
    assert suscriptions_response[0]['id_event'] == all_events_data[0]['id']
    assert suscriptions_response[1]['id_event'] == all_events_data[1]['id']
